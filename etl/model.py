class Filter:
    """
    Represents targeting parameters for Transactions to perform custom ETL
    """

    def __init__(self, starts_with=None, includes=None, ends_with=None):
        self.starts_with = starts_with
        self.includes = includes
        self.ends_with = ends_with


class Transformation:
    """
    Transformation to apply to a transaction during a custom ETL.
    The category, sub category and name are all optional, and the absence
    of a value results in no change to the transaction.
    """

    def __init__(self, my_category, my_sub_category, name):
        self.my_category = my_category
        self.my_sub_category = my_sub_category
        self.name = name


class CustomETL:
    """
    Custom ETL operation
    """

    def __init__(self, filter, transformation):
        self.filter = filter
        self.transformation = transformation
