import os
from typing import List

from util.logger import get_logger


class ObsidianClient:
    def __init__(self, config):
        self.vault_path = config["obsidian_vault_path"]
        self.logger = get_logger("obsidian", config["log_level"])

    def build_file_name(self, transaction: dict) -> str:
        """Build a filename for the transaction based on its date and name."""
        transaction_id = transaction["transaction_id"]
        year, month, day = self.get_tx_date(transaction)
        return f"{year}{month}{day}-{transaction_id}.md"

    def get_tx_date(self, transaction: dict):
        """Get the date of the transaction in YYYY-MM format."""
        tx_date = transaction["date"]
        # If tx_date is a datetime, then convert it to a string
        if not isinstance(tx_date, str):
            tx_date = tx_date.strftime("%Y-%m-%d")
        return tx_date[:4], tx_date[5:7], tx_date[8:10]

    def get_year_month_folder(self, transaction: dict) -> str:
        """Get the date of the transaction in YYYY-MM format."""
        year, month, _ = self.get_tx_date(transaction)
        return f"{year}/{month}"

    def filter_existing_transactions(self, transactions) -> List[dict]:
        """
        The function filters out existing transactions from a given array of transactions
          based on the files being present in the Obsidian vault.
        """
        if len(transactions) == 0:
            return transactions
        # Since transactions are handled on a month by month basis,
        # then get the year and month folder based on the date of the first transaction
        year_month_folder = self.get_year_month_folder(transactions[0])
        folder_path = os.path.join(self.vault_path, year_month_folder)
        self.logger.info(f"Looking for existing transactions in folder: {folder_path}")
        existing_tx_ids = set()
        if os.path.exists(folder_path):
            for tx in transactions:
                filename = self.build_file_name(tx)
                if os.path.exists(os.path.join(folder_path, filename)):
                    existing_tx_ids.add(tx["transaction_id"])

        new_transactions = [
            tx for tx in transactions if tx["transaction_id"] not in existing_tx_ids
        ]
        return new_transactions

    def write_transactions(self, transactions):
        """
        The function writes the given transactions to the Obsidian vault.
        """
        self.logger.info(
            f"Writing {len(transactions)} transactions to Obsidian vault at {self.vault_path}"
        )

        year_month_folder = self.get_year_month_folder(transactions[0])
        folder_path = os.path.join(self.vault_path, year_month_folder)
        os.makedirs(folder_path, exist_ok=True)

        # For every new transaction, build the content and write the file
        for tx in transactions:
            filename = self.build_file_name(tx)
            file_path = os.path.join(folder_path, filename)
            content = self.build_transaction_content(tx)
            with open(file_path, "w") as f:
                f.write(content)
            self.logger.info(f"Wrote transaction to {file_path}")

    def build_transaction_content(self, transaction: dict) -> str:
        """Build the content of the markdown file for the transaction."""
        # The name may have additional colons, and those will mess up the frontmatter,
        # so replace all of them with hyphens
        while ":" in transaction["name"]:
            transaction["name"] = transaction["name"].replace(":", "-")
            
        return f"""---
date: {transaction["date"]}
description: {transaction["name"]}
amount: {transaction["amount"]}
category: {transaction.get("my_category")}
subcategory: {transaction.get("my_sub_category")}
reviewed: {'true' if transaction.get("checked") == 'y' else ''}
---

Raw Category: {transaction["my_raw_category"]}
Account: {transaction["account_owner"]}
Transaction Id: {transaction["transaction_id"]}

"""
