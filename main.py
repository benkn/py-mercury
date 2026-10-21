from typing import List
from config.config import Config
from config.accounts import accounts
from etl.decorate import decorate_transactions
from etl.to_column_format import to_columns
from services.google_sheets import GoogleSheetsClient
from services.plaid import PlaidAuthExpiredError, PlaidClient, PlaidError
from services.obsidian import ObsidianClient
from services.slack import SlackClient

from util.logger import get_logger

logger = get_logger("mercury", Config["log_level"])


def main():
    logger.info("Mercury rising!")
    logger.debug("Processing %d Accounts", len(accounts))

    plaidClient = PlaidClient(Config)

    # Get all transactions from all accounts
    allTransactions: List[dict] = []
    failures: List[str] = []

    for account in accounts:
        logger.info(f"Reading from {account.name}")
        try:
            transactions: List[dict] = plaidClient.get_transactions(
                account, Config["start_date"], Config["end_date"]
            )
        except PlaidAuthExpiredError as exc:
            logger.error("%s Re-link it with Plaid Link update mode. (%s)", exc, exc.error)
            failures.append(f":key: {exc}")
            continue
        except PlaidError as exc:
            logger.error("%s (%s)", exc, exc.error)
            failures.append(f":warning: {exc}")
            continue
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

    if failures:
        SlackClient(Config).send_alert(
            "Mercury skipped some accounts:\n" + "\n".join(failures)
        )

    logger.info("All done!")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        logger.exception("Mercury failed")
        SlackClient(Config).send_alert(f":rotating_light: Mercury failed: {exc}")
        raise
