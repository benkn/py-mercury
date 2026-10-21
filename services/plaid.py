import plaid
import json
from plaid.api import plaid_api
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.item_remove_request import ItemRemoveRequest

from util.logger import get_logger

# Plaid error codes meaning the Item's credentials/OAuth consent must be refreshed via Link update mode.
AUTH_EXPIRED_ERROR_CODES = {"ITEM_LOGIN_REQUIRED", "INVALID_ACCESS_TOKEN"}


class PlaidError(Exception):
    def __init__(self, message, error=None):
        super().__init__(message)
        self.error = error


class PlaidAuthExpiredError(PlaidError):
    pass


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
            error = format_error(e)["error"]
            if error["error_code"] in AUTH_EXPIRED_ERROR_CODES:
                raise PlaidAuthExpiredError(
                    f"The auth for {account.name} has expired.", error
                ) from None
            raise PlaidError(
                f"Failed to get transactions for {account.name}: {error['display_message']}",
                error,
            ) from None

    def remove_item(self, account):
        self.logger.info("Removing item for %s", account.name)
        try:
            request = ItemRemoveRequest(access_token=account.access_token)
            response = self.client.item_remove(request).to_dict()
            self.logger.info("Removed item for %s", account.name)
            return response
        except plaid.ApiException as e:
            error_response = format_error(e)
            self.logger.error("Failed to remove item: %s", error_response)
            return error_response

    def pretty_print_response(self, response):
        self.logger.debug(json.dumps(response, indent=2, sort_keys=True, default=str))


def format_error(e):
    try:
        response = json.loads(e.body)
    except (TypeError, ValueError):
        response = {}
    return {
        "error": {
            "status_code": e.status,
            "display_message": response.get("error_message", e.reason),
            "error_code": response.get("error_code"),
            "error_code_reason": response.get("error_code_reason"),
            "error_type": response.get("error_type"),
        }
    }
