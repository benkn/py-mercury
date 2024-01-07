from etl.model import CustomETL, Filter, Transformation

# This is an example of the list of ETL operations which you can
# perform with Mercury. Transformations happen to transactions on the
# first match with a custom ETL rule.
#
# Copy this file to customRules.py and include your own ETL operations.
custom_etls = [
    CustomETL(
        filter=Filter(starts_with="CHASE CREDIT CRD DES:AUTOPAY"),
        transformation=Transformation(
            my_category="Credit Card Payment",
            my_sub_category="",
            name="Chase Credit Card Payment",
        ),
    ),
    CustomETL(
        filter=Filter(starts_with="BEN GONGS TEA"),
        transformation=Transformation(
            my_category="Food and Drink",
            my_sub_category="Coffee Shops",
            name="Ben Gongs Tea",
        ),
    ),
]
