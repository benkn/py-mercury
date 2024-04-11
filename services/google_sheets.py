import gspread
from util.logger import get_logger


class GoogleSheetsClient:
    def __init__(self, config):
        self.gc = gspread.service_account(config["google_credentials"])
        self.sh = self.gc.open_by_key(config["spreadsheet_id"])
        self.sheet_index = config["spreadsheet_index"]
        self.logger = get_logger("GoogleSheetsClient", config["log_level"])

    def find_removed_transactions(self, transactions, existing_tx_ids):
        # Create a set of ids for transactions
        transaction_ids = set(map(lambda tx: tx["transaction_id"], transactions))

        # Any ID found in the existing IDs but not in the transaction IDs should be removed
        tx_ids_to_remove = set(
            filter(lambda tx_id: tx_id not in transaction_ids and tx_id > '', existing_tx_ids)
        )

        if len(tx_ids_to_remove) > 0:
            self.logger.info(
                "The following transaction IDs are in the sheet, but not expected. They should be deleted."
            )
            self.logger.info(tx_ids_to_remove)

    def filter_existing_transactions(self, transactions):
        """The function filters out existing transactions from a given array of transactions based on the data in a Google Sheets spreadsheet."""
        worksheet = self.sh.get_worksheet(self.sheet_index)
        # retrieve existing records as a list of dictionaries
        existing_txs = worksheet.get_all_records()
        existing_tx_ids = set(
            map(lambda row: row.get("Transaction ID"), existing_txs[0:])
        )
        self.logger.debug("Existing transaction IDs:")
        self.logger.debug(existing_tx_ids)

        self.find_removed_transactions(transactions, existing_tx_ids)

        new_transactions = [
            tx for tx in transactions if tx["transaction_id"] not in existing_tx_ids
        ]

        return new_transactions

    def append_to_sheet(self, rows):
        """The function writes the given rows to the sheet"""
        worksheet = self.sh.get_worksheet(self.sheet_index)
        # "USER_ENTERED" prevents prefixed apostraphes on the date
        worksheet.append_rows(rows, "USER_ENTERED")
