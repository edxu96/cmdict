"""Test functions to check English or German spelling."""
from cmdict.check import check_de


def test_check_de():
    """See if correct and incorrect German words can be checked.

    Note:
        Capitalisation in German is not supported here, because they are
        all returned in lower case.
    """
    assert check_de("Dank") == "dank"
    assert check_de("Danke") == "danke"
    assert check_de("Dant") == "dann"
    assert check_de("dank") == "dank"

    assert check_de("schlafe") == "schlafe"
    assert check_de("schlafee") == "schlafen"
    assert check_de("schläfst") == "schläfst"

    assert check_de("Schläfst") == "schläfst"
