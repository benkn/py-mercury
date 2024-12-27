from etl.apply_custom_rule import apply_custom_rule
from etl.custom_categories import CategoryLookups, SubCategoryLookups
from util.readable import readable


def decorate_transactions(transactions):
    [decorate_transaction(t) for t in transactions]


def decorate_transaction(transaction: dict):
    transaction["my_category"] = None
    transaction["my_sub_category"] = None
    transaction["my_raw_category"] = None
    transaction["checked"] = ""

    if apply_custom_rule(transaction):
        transaction["checked"] = "y"
        return  # behavior complete, end function

    # If the transaction has a personal finance category, then decorate accordingly
    elif transaction.get("personal_finance_category"):
        primary = transaction["personal_finance_category"]["primary"].strip()
        detailed = transaction["personal_finance_category"]["detailed"].strip()
        primary_length = len(primary)
        subcategory = detailed[primary_length:]
        transaction["my_raw_category"] = detailed

        # If we have an override for the category based on the detailed category given by Plaid, then set it as the category
        if CategoryLookups.get(detailed):
            transaction["my_category"] = CategoryLookups[detailed]
            transaction["checked"] = "y"
            if SubCategoryLookups.get(detailed):
                transaction["my_sub_category"] = SubCategoryLookups[detailed]
            else:
                transaction["my_sub_category"] = readable(subcategory)

        # Else, if there is a replacement for the subcategory, set it
        elif SubCategoryLookups.get(detailed):
            transaction["my_category"] = readable(primary)
            transaction["my_sub_category"] = SubCategoryLookups[detailed]

        elif (
            transaction["personal_finance_category"]["confidence_level"] == "VERY_HIGH"
        ):
            transaction["my_category"] = readable(primary)
            transaction["my_sub_category"] = readable(subcategory)
            # if the confidence level is very high, and not General Merchandise (which can lead to false positives)
            if transaction["my_category"] != "General Merchandise":
                transaction["checked"] = "y"

        elif transaction["personal_finance_category"]["confidence_level"] == "HIGH":
            transaction["my_category"] = readable(primary)
            transaction["my_sub_category"] = readable(subcategory)

        # If confidence is not high, then it probably needs a follow up
        else:
            transaction["my_category"] = "Maybe... " + readable(primary)
            transaction["my_sub_category"] = readable(subcategory)

    # If all else fails, then just mark is Unknown for a further follow-up
    else:
        transaction["my_category"] = "Unknown"

    return transaction
