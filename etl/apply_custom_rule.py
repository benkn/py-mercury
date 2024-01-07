from etl.custom_etls import custom_etls
from util.first_defined import first_defined
from util.readable import readable


def apply_custom_rule(transaction):
    """
    Reviews custom rules to see if any apply to this transaction.
    For the first one which matches, apply transformations to the transaction and return true.
    """
    for etl in custom_etls:
        if matches_filter(transaction, etl.filter):
            primary = (
                transaction["personal_finance_category"]["primary"]
                if transaction.get("personal_finance_category")
                else ""
            )
            detailed = (
                transaction["personal_finance_category"]["detailed"]
                if transaction.get("personal_finance_category")
                else ""
            )

            subCategory = detailed[len(primary) :]
            transaction["my_raw_category"] = detailed

            transaction["my_category"] = first_defined(
                etl.transformation.my_category, readable(primary)
            )
            transaction["my_sub_category"] = first_defined(
                etl.transformation.my_sub_category, readable(subCategory)
            )
            transaction["name"] = (
                etl.transformation.name
                if etl.transformation.name
                else transaction["name"]
            )

            # once one rule matches, end
            return True
    # No custom rules applied!
    return False


def matches_filter(transaction, filter):
    """
    Reviews the filter rules for this transaction and returns true if the transaction matches the rules.
    """
    t_name = transaction["name"]
    starts_with = (
        t_name.upper().startswith(filter.starts_with.upper())
        if filter.starts_with != None
        else True
    )
    includes = (
        filter.includes.upper() in t_name.upper() if filter.includes != None else True
    )
    ends_with = (
        t_name.upper().endswith(filter.ends_with.upper())
        if filter.ends_with != None
        else True
    )
    return starts_with and includes and ends_with
