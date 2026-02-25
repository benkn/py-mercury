from typing import List
from config.config import Config
from config.accounts import accounts
from etl.decorate import decorate_transactions
from etl.to_column_format import to_columns
from services.google_sheets import GoogleSheetsClient
from services.plaid import PlaidClient
from services.obsidian import ObsidianClient

from util.logger import get_logger

logger = get_logger("mercury", Config["log_level"])

logger.info("Mercury rising!")
logger.debug("Processing %d Accounts", len(accounts))

plaidClient = PlaidClient(Config)

# Get all transactions from all accounts
allTransactions: List[dict] = []

for account in accounts:
    logger.info(f"Reading from {account.name}")
    transactions: List[dict] = plaidClient.get_transactions(
        account, Config["start_date"], Config["end_date"]
    )
    for t in transactions:
        t["account_owner"] = account.name
    allTransactions.extend(transactions)
    logger.info("Total transactions found so far: %d", len(allTransactions))

if Config["output"] == "obsidian":
    obsidian_client = ObsidianClient(Config)
    new_transactions: List[dict] = obsidian_client.filter_existing_transactions(
        allTransactions
    )
    if len(new_transactions) > 0:
        logger.info(
            "Found %d new transactions. Decorating them and turning them into rows.",
            len(new_transactions),
        )
        decorate_transactions(new_transactions)
        obsidian_client.write_transactions(new_transactions)
    else:
        logger.info("No new transactions")

else:
    logger.info("Preparing to write to Google Sheets")
    # Write to Google Sheets
    google_sheets_client = GoogleSheetsClient(Config)

    logger.info("Removing existing transactions")
    new_transactions: List[dict] = google_sheets_client.filter_existing_transactions(
        allTransactions
    )

    if len(new_transactions) > 0:
        logger.info(
            "Found %d new transactions. Decorating them and turning them into rows.",
            len(new_transactions),
        )
        decorate_transactions(new_transactions)

        rows: List[str] = to_columns(new_transactions)
        logger.info("Writing transactions to the budget sheet")
        google_sheets_client.append_to_sheet(rows)
    else:
        logger.info("No new transactions")

logger.info("All done!")
