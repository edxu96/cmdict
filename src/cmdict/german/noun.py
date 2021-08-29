"""Class for German noun."""
from enum import Enum

from cmdict.german.spelling import InflectedWordForm, Word
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

    .. [hammer2017german] Durrell, M. (2017). Hammer's German grammar
        and usage. Routledge.
    """

    M = "masculine"
    F = "feminine"
    N = "neuter"


class NounCase(Enum):
    """Enumeration for four cases of an (inflected) German noun."""

    N = "norminativ"
    G = "gernitiv"
    D = "dativ"
    A = "akkusativ"


class DeclensionMethod(Enum):
    """Enumeration for eight ways to inflect a German noun."""

    NS = (NounCase.N, True)  # "Norminativ Singular"
    NP = (NounCase.N, False)  # "Norminativ Plural"
    GS = (NounCase.G, True)  # "Gernitiv Singular"
    GP = (NounCase.G, False)  # "Gernitiv Plural"
    DS = (NounCase.D, True)  # "Dativ Singuler"
    DP = (NounCase.D, False)  # "Dativ Plural"
    AS = (NounCase.A, True)  # "Akkusativ Singuler"
    AP = (NounCase.A, False)  # "Akkusativ Plural"


class Declension(InflectedWordForm):
    """Represent one declension of a German noun."""

    def __init__(
        self, spelling: str, origin: str, singular: bool, case: NounCase
    ) -> None:
        """Init a declension based on detailed declension method.

        Args:
            spelling: how this inflected word is spelled.
            origin: the original word form of this word.
            singular: whether this word is singular.
            case: which case this word represents.
        """
        super().__init__(spelling, origin=origin)

        self.singular = singular
        self.case = case

    @classmethod
    def from_method(
        cls, spelling: str, origin: str, declension: DeclensionMethod
    ):
        """Init a declension based on basic info and declension method.

        Args:
            spelling: how the declension is spelled.
            origin: how the original form is spelled.
            declension: which declension method is used.

        Returns:
            An object storing detailed declension method, IPA, and
            syllabification.
        """
        return cls(
            spelling=spelling,
            origin=origin,
            singular=declension.value[1],
            case=declension.value[0],
        )


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

        self.gender = Gender.N
        """Gender: which grammatical gender this word belongs to."""

        self.articles = {}
        """Dict[str, str]: article for each declension."""
        self.spellings = {}
        """Dict[str, List[str]]: spelling(s) for each declension."""
        self.declensions = {}
        """Dict[str, List[str]]: inflected form for each declension."""

        self.soup = self.crawl_wiktionary()
        self._assign_tables()

    def _assign_tables(self):
        """Store table for eight forms of a German noun in two dicts.

        Warning:
            It is assumed that one cell can have two spellings at most.
        """
        table = self.soup.find("table", class_=_CLASS_TABLE).find("tbody")

        articles = {}
        spellings = {}
        declensions = {}
        iter_form = iter(DeclensionMethod)
        for row in table.find_all("tr")[1:5]:
            for cell in row.find_all("td")[0:2]:
                article = cell.text.split(" ")[0]
                how_declension = next(iter_form)
                # There might be two word forms in one cell.
                if len(cell.find_all()) >= 2:
                    spelling_list = [
                        remove_newline(cell.text.split(article + " ")[i])
                        for i in [1, 2]
                    ]
                    declension_list = [
                        Declension.from_method(
                            spelling, self.spelling, how_declension
                        )
                        for spelling in spelling_list
                    ]
                else:
                    spelling = remove_newline(
                        cell.text.split(article + " ")[1]
                    )
                    spelling_list = [spelling]
                    declension_list = [
                        Declension.from_method(
                            spelling, self.spelling, how_declension
                        )
                    ]

                spellings[how_declension] = spelling_list
                articles[how_declension] = article
                declensions[how_declension] = declension_list

        self.articles = articles
        self.spellings = spellings
        self.declensions = declensions

    def to_adoc(self) -> str:
        """Print eight forms of German noun in Asciidoc-friendly format.

        Returns:
            Eight forms of German noun in Asciidoc-friendly format.
        """
        content = ""

        iter_form = iter(DeclensionMethod)
        for i in range(4):
            row = ""
            for j in range(2):
                declension = next(iter_form)
                row += f"|{self.articles[declension]} "
                row += "|" + ", ".join(self.spellings[declension]) + " "
            content += row + "\n"

        res = _ADOC.format(content=content)
        return res
