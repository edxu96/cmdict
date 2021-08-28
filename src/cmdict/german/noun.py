"""Class for German noun."""
from enum import Enum

from cmdict.german.spelling import Word
from cmdict.utils import remove_newline

_CLASS_TABLE = (
    "wikitable float-right inflection-table flexbox " + "hintergrundfarbe2"
)
_ADOC = """
[cols="1,1,1,1"]
|===
|Singular |Spelling |Singular |Spelling

{content}|===
"""


class Gender(Enum):
    """Enumeration for three German grammar genders.

    The concept of grammatical gender in German is discussed in
    [hammer2017german]_:

        "Grammatical gender is a system for classifying nouns. It is not
        the same as 'natural' gender (i.e. 'males', 'females' and
        'things', as in English), and for this reason the names of the
        genders in German are rather misleading and the classification
        can seem arbitrary to English learners, especially as words for
        'things' can have any gender".

    """

    M = "masculine"
    F = "feminine"
    N = "neuter"


class Case(Enum):
    """Enumeration for four cases for German noun."""

    N = "norminativ"
    G = "gernitiv"
    D = "dativ"
    A = "akkusativ"


class NumberNoun(Enum):
    """Enumeration for number represented by a German noun."""

    S = "singuler"
    P = "plural"


class FormNoun(Enum):
    """Enumeration for eight forms of a German noun."""

    NS = "Norminativ Singular"
    NP = "Norminativ Plural"
    GS = "Gernitiv Singular"
    GP = "Gernitiv Plural"
    DS = "Dativ Singuler"
    DP = "Dativ Plural"
    AS = "Akkusativ Singuler"
    AP = "Akkusativ Plural"


class Noun(Word):
    """Represent a German noun.

    For every noun, there are three grammatical features:

    - Gender: ``masculine``, ``feminine``, or ``neuter``.
    - Number: ``singular`` or ``plural``.
    - Case.
    """

    def __init__(self, checked: str) -> None:
        """Init for a German noun based on its spelling.

        Args:
            checked: a checked spelling for a German noun in lower case.
        """
        # Capitalise the first letter.
        word = checked[:1].upper() + checked[1:]

        super().__init__(word)

        self.articles = None
        self.spellings = None

        self.soup = self.crawl()
        self._assign_tables()

    def _assign_tables(self):
        """Store table for eight forms of a German noun in two dicts.

        Warning:
            It is assumed that one cell can have two spellings at most.
        """
        table = self.soup.find("table", class_=_CLASS_TABLE).find("tbody")

        articles = {}
        spellings = {}
        iter_form = iter(FormNoun)
        for row in table.find_all("tr")[1:5]:
            for cell in row.find_all("td")[0:2]:
                article = cell.text.split(" ")[0]
                # There might be two forms in one cell.
                if len(cell.find_all()) >= 2:
                    spelling_1 = remove_newline(
                        cell.text.split(article + " ")[1]
                    )
                    spelling_2 = remove_newline(
                        cell.text.split(article + " ")[2]
                    )
                    spelling = [spelling_1, spelling_2]
                else:
                    spelling = [
                        remove_newline(cell.text.split(article + " ")[1])
                    ]

                which_form = next(iter_form)
                spellings[which_form] = spelling
                articles[which_form] = article

        self.articles = articles
        self.spellings = spellings

    def to_adoc(self) -> str:
        """Print eight forms of German noun in Asciidoc-friendly format.

        Returns:
            Eight forms of German noun in Asciidoc-friendly format.
        """
        content = ""

        iter_form = iter(FormNoun)
        for i in range(4):
            row = ""
            for j in range(2):
                form = next(iter_form)
                row += f"|{self.articles[form]} "
                row += "|" + ", ".join(self.spellings[form]) + " "
            content += row + "\n"

        res = _ADOC.format(content=content)
        return res
