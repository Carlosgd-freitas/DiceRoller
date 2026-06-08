import unicodedata


def unaccent(text: str) -> str:
    """
    Removes all accents from a string.

    :var text: A string.
    :vartype text: str

    :return: An unaccented string.
    :rtype: str
    """
    return "".join(
        c for c in unicodedata.normalize("NFD", text) if not unicodedata.combining(c)
    )


def normalize(text: str) -> str:
    """
    Normalizes a string, removing all accents from it and converting it into lowercase.

    :var text: A string.
    :vartype text: str

    :return: A normalized string.
    :rtype: str
    """
    return unaccent(text).lower()
