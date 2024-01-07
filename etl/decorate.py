from etl.apply_custom_rule import apply_custom_rule
from etl.customCategories import CategoryLookups, SubCategoryLookups
from util.readable import readable


def decorateTransactions(transactionsList):
    [decorateTransaction(t) for t in transactionsList]


def decorateTransaction(transaction):
    transaction["my_category"] = None
    transaction["my_sub_category"] = None
    transaction["my_raw_category"] = None

    if apply_custom_rule(transaction):
        return  # behavior complete, end function

    # If the transaction has a personal finance category, then decorate accordingly
    elif transaction.get("personal_finance_category"):
        primary = transaction["personal_finance_category"]["primary"].strip()
        detailed = transaction["personal_finance_category"]["detailed"].strip()
        primaryLength = len(primary)
        subCategory = detailed[primaryLength:]
        transaction["my_raw_category"] = detailed

        # If we have an override for the category based on the detailed category given by Plaid, then set it as the category
        if CategoryLookups.get(detailed):
            transaction["my_category"] = CategoryLookups[detailed]
            if SubCategoryLookups.get(detailed):
                transaction["my_sub_category"] = SubCategoryLookups[detailed]
            else:
                transaction["my_sub_category"] = readable(subCategory)

        # Else, if there is a replacement for the subcategory, set it
        elif SubCategoryLookups.get(detailed):
            transaction["my_category"] = readable(primary)
            transaction["my_sub_category"] = SubCategoryLookups[detailed]

        elif (
            transaction["personal_finance_category"]["confidence_level"] == "VERY_HIGH"
            or transaction["personal_finance_category"]["confidence_level"] == "HIGH"
        ):
            transaction["my_category"] = readable(primary)
            transaction["my_sub_category"] = readable(subCategory)

        # If confidence is not high, then it probably needs a follow up
        else:
            transaction["my_category"] = "Maybe... " + readable(primary)
            transaction["my_sub_category"] = readable(subCategory)

    # If all else fails, then just mark is Unknown for a further follow-up
    else:
        transaction["my_category"] = "Unknown"

    return transaction
