from config.config import Config
from config.accounts import accounts
from etl.decorate import decorate_transactions
from etl.toColumnFormat import to_columns
from services.googleSheets import GoogleSheetsClient
from services.plaid import PlaidClient

from util.logger import get_logger

logger = get_logger("mercury", Config["log_level"])

logger.info("Mercury rising!")
logger.debug("Processing %d Accounts", len(accounts))

plaidClient = PlaidClient(Config)

allTransactions = []
for account in accounts:
    transactions = plaidClient.get_transactions(
        account, Config["start_date"], Config["end_date"]
    )
    for t in transactions:
        t["account_owner"] = account.name
    allTransactions.extend(transactions)
    logger.info("Total transactions found so far: %d", len(allTransactions))

google_sheets_client = GoogleSheetsClient(Config)

logger.info("Removing existing transactions")
new_transactions = google_sheets_client.filter_existing_transactions(allTransactions)

if len(new_transactions) > 0:
    logger.info(
        "Found %d new transactions. Decorating them and turning them into rows.",
        len(new_transactions),
    )
    decorate_transactions(new_transactions)

    rows = to_columns(new_transactions)
    logger.info("Writing transactions to the budget sheet")
    google_sheets_client.append_to_sheet(rows)
else:
    logger.info("No new transactions")

logger.info("All done!")
