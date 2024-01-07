skipWords = set(["AND"])


def readable(categoryName):
    """
    Takes a string and splits it by underscores and capitalizes key words.
    Categories by Plaid are formatted in uppercase with words separated by underscores.
    """
    parts = categoryName.split("_")
    return " ".join(list(map(lambda part: capitalize(part), parts))).strip()


def capitalize(str):
    """
    Capitalize the given string
    """
    if str in skipWords:
        return str.lower()

    return str[0].upper() + str[1:].lower()
