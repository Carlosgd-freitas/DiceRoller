import unicodedata
from math import inf


def numeric_to_string(value: float) -> str:
    """
    Casts a numeric value to string.

    :param value: A numeric value.
    :type value: float

    :return: A string.
    :rtype: str
    """
    if value is None:
        return None

    if isinstance(value, str):
        return value
    elif value != inf:
        return f"{value:g}"
    else:
        return "∞"


def unaccent(text: str) -> str:
    """
    Removes all accents from a string.

    :var text: A string.
    :vartype text: str

    :return: An unaccented string.
    :rtype: str
    """
    if text is None:
        return None

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
    if text is None:
        return None

    return unaccent(text).lower()


def normalize_filename(filename: str, extension: str) -> str:
    """
    Normalizes a filename, unaccenting it and including a file extension, if does
    not have one.

    :param filename: Filename.
    :type filename: str

    :param extension: Filename extension, including the '.' (e.g. '.dat').
    :type extension: str

    :return: Normalized filename.
    :rtype: str
    """
    if filename is None or extension is None:
        return None

    normalized = normalize(filename).replace(" ", "_")

    if not normalized.endswith(extension):
        normalized += extension

    return normalized
