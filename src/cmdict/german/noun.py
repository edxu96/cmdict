"""Class for German noun."""
from loguru import logger

from cmdict.german.article import (
    ARTICLES_DEF,
    Case,
    Declension,
    DeclensionMethod,
    Gender,
)
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
_GENDER = {"m": Gender.M, "f": Gender.F, "n": Gender.N}


class DeclensionNoun(Declension):
    """Represent (inflected) form of a German noun."""

    def __init__(
        self,
        spelling: str,
        origin: str,
        singular: bool,
        gender: Gender,
        case: Case,
    ) -> None:
        """Init based on attribute and find its gender and articles.

        Args:
            spelling: how this inflected word is spelled.
            origin: the original word form of this word. None if this
                word form is the origin.
            singular: whether this word is singular.
            gender: which grammatical gender this word belongs to.
            case: which case this word represents.
        """
        super().__init__(spelling, origin, singular, gender, case)

        #: Declension: corresponding definite article.
        self.article_def = None

        self._find_gender()
        self._find_articles()

    def _find_articles(self):
        """Find corresponding definite and indefinite article."""
        if not self.singular:
            the_key = (self.singular, Gender.X, self.case)
        else:
            the_key = (self.singular, self.gender, self.case)

        self.article_def = ARTICLES_DEF[the_key]

    def _find_gender(self):
        """Find gender in crawled ``wiktionary`` and assign the value."""
        try:
            text_raw = (
                self.soup.find("h3").find("span", class_="mw-headline").text
            )
            gender_raw = text_raw.split(", ")[1]
            self.gender = _GENDER[gender_raw]
        except (AttributeError, KeyError):
            logger.critical(f"Gender for {self.spelling} is not found.")
            self.gender = None


class Noun(DeclensionNoun):
    """Represent a singular nominative German noun served as origin.

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

        super().__init__(word, None, True, None, Case.N)

        self.articles = {}
        """Dict[str, str]: article for each declension."""
        self.spellings = {}
        """Dict[str, List[str]]: spelling(s) for each declension."""
        self.declensions = {}
        """Dict[str, List[str]]: inflected form for each declension."""

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
                            spelling,
                            self.spelling,
                            how_declension,
                            self.gender,
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
                            spelling,
                            self.spelling,
                            how_declension,
                            self.gender,
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
