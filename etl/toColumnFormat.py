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


def to_columns(transaction_list):
    rows = list()

    if len(transaction_list) > 0:
        for t in transaction_list:
            rows.append(
                [
                    str(t["date"]),
                    t["name"],
                    t["amount"],
                    "",
                    t["my_category"],
                    t["my_sub_category"],
                    t["account_owner"],
                    t["my_raw_category"],
                    t["transaction_id"],
                ]
            )

    return rows


def print_rows(rows):
    for row in rows:
        print(",".join(row))
