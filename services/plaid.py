import plaid
import json
from plaid.api import plaid_api
from plaid.model.transactions_get_request import TransactionsGetRequest

from util.logger import get_logger


class PlaidClient:
    def __init__(self, config):
        self.config = config
        self.logger = get_logger("plaid", config["log_level"])

        host = plaid.Environment.Sandbox

        if config["plaid"]["env"] == "sandbox":
            host = plaid.Environment.Sandbox

        if config["plaid"]["env"] == "development":
            host = plaid.Environment.Development

        if config["plaid"]["env"] == "production":
            host = plaid.Environment.Production

        configuration = plaid.Configuration(
            host=host,
            api_key={
                "clientId": config["plaid"]["client_id"],
                "secret": config["plaid"]["secret"],
                "plaidVersion": config["plaid"]["version"],
            },
        )

        api_client = plaid.ApiClient(configuration)
        self.client = plaid_api.PlaidApi(api_client)

    def get_transactions(self, account, startDate, endDate):
        self.logger.info("Fetching transactions for %s", account.name)
        try:
            request = TransactionsGetRequest(
                access_token=account.access_token,
                start_date=startDate,
                end_date=endDate,
                options={"count": 500},
            )
            response = self.client.transactions_get(request).to_dict()
            total_transactions = response["total_transactions"]
            transactions = response["transactions"]

            self.logger.info("Received %d transactions.", total_transactions)

            filteredTransactions = list(
                filter(
                    # Filtear transactions with amounts outside of config requirements
                    lambda t: t["amount"] <= self.config["max_value_to_include"]
                    or t["amount"] >= 1000,
                    # Filter pending transactions
                    filter(lambda t: not t["pending"], transactions),
                )
            )

            self.pretty_print_response(filteredTransactions)

            return filteredTransactions

        except plaid.ApiException as e:
            error_response = format_error(e)
            self.logger.error("Failed to get transactions: %s", error_response.__dict__)
            return error_response

    def pretty_print_response(self, response):
        self.logger.debug(json.dumps(response, indent=2, sort_keys=True, default=str))


def format_error(e):
    response = json.loads(e.body)
    return {
        "error": {
            "status_code": e.status,
            "display_message": response["error_message"],
            "error_code": response["error_code"],
            "error_type": response["error_type"],
        }
    }
