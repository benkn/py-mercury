import gspread


class GoogleSheetsClient:
    def __init__(self, config):
        self.gc = gspread.service_account_from_dict(config["google_credentials"])
        self.sh = self.gc.open_by_key(config["spreadsheet_id"])
        self.sheet_index = config["spreadsheet_index"]

    def find_removed_transactions(self, transactions, existing_tx_ids):
        # Create a set of ids for transactions
        transaction_ids = set(map(lambda t: t["transaction_id"], transactions))

        # Any ID found in the existing IDs but not in the transaction IDs should be removed
        tx_ids_to_remove = list(
            filter(lambda tx_id: tx_id not in transaction_ids, existing_tx_ids)
        )

        if len(tx_ids_to_remove) > 0:
            print(
                "The following transaction IDs are in the sheet, but not expected. They should be deleted."
            )
            print(tx_ids_to_remove)

    def filter_existing_transactions(self, transactions):
        """The function filters out existing transactions from a given array of transactions based on the data in a Google Sheets spreadsheet."""
        worksheet = self.sh.get_worksheet(self.sheet_index)
        # print("Using worksheet")
        # print(worksheet)
        # retrieve existing records as a list of dictionaries
        existing_txs = worksheet.get_all_records()
        existing_tx_ids = set(
            map(lambda row: row.get("Transaction ID"), existing_txs[1:])
        )

        self.find_removed_transactions(transactions, existing_tx_ids)

        return list(filter(lambda tx: tx.get("transaction_id"), transactions))

    def append_to_sheet(self, rows):
        """The function writes the given rows to the sheet"""
        worksheet = self.sh.get_worksheet(2)
        worksheet.append_rows(rows)
