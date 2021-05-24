"""Utility functions."""
import string

SPECIAL_CHARS = "“”"


def remove_punctuation(s):
    """Remove all kinds of punctuations in the string.

    Args:
        s (str): to be removed from punctuations.

    Returns:
        str: with all kinds of punctuation removed.
    """
    table = str.maketrans("", "", string.punctuation + SPECIAL_CHARS)
    return s.translate(table)


def remove_newline(s):
    r"""Remove newline escape ``\n`` in a given string.

    Args:
        s (str): some string might containing none/one/multiple newline
            escapes.

    Returns:
        str: the string without any newline escape.
    """
    splits = s.split("\n")
    res = ""
    for split in splits:
        res += split
    return res


def remove_cdot(s):
    """Remove central dot if any in a syllabified spelling.

    Args:
        s (str): some string might containing central dot(s).

    Returns:
        str: the string without any central dot.
    """
    res = s.replace("·", "")
    return res
