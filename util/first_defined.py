def first_defined(x, y):
    """
    Returns the first value in the parameters which has been defined.
    """
    return x if x is not None else y
