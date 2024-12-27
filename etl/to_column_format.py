from typing import List


headerRow = [
    "Date",
    "Description",
    "Amount",
    "✅",
    "Category",
    "Sub-Category",
    "Account",
    "Raw Category",
    "Transaction ID",
]


def to_columns(transaction_list: dict) -> List[str]:
    rows = list()

    if len(transaction_list) > 0:
        for tx in transaction_list:
            rows.append(
                [
                    str(tx["date"]),
                    tx["name"],
                    tx["amount"],
                    tx["checked"],
                    tx["my_category"],
                    tx["my_sub_category"],
                    tx["account_owner"],
                    tx["my_raw_category"],
                    tx["transaction_id"],
                ]
            )

    return rows


def print_rows(rows):
    for row in rows:
        print(",".join(row))
