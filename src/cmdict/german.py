"""Classes for German verbs and nouns."""
from enum import Enum
from typing import Optional, Tuple

from bs4 import BeautifulSoup
from loguru import logger
import requests

from cmdict.check import check_de
from cmdict.utils import remove_cdot, remove_newline

_LINK_REVERSO = (
    "https://conjugator.reverso.net/" + "conjugation-german-verb-{origin}.html"
)
_PRESENT = {
    "ich": None,
    "du": None,
    "er": None,
    "wir": None,
    "ihr": None,
    "sie": None,
}
_PRESENT_LIST = ["ich", "du", "er", "wir", "ihr", "sie"]
_PRINT_PRESENT = {
    "ich": "ich",
    "du": "du",
    "er": "er/sie/es",
    "wir": "wir",
    "ihr": "ihr",
    "sie": "Sie",
}
_HEADERS_PRESENT = ["Präsens", "Spelling", "IPA"]
_FRAME_ADOC = """
[cols="1,1,1"]
|===
|Personalpronomen |Spelling |IPA

{content}|===
"""
_ATTRS_SYLLABIFICATION = {"title": "Trennungsmöglichkeiten am Zeilenumbruch"}
_LINK_WIKI = "https://de.wiktionary.org/wiki/{word}"
_CLASS_TABLE = (
    "wikitable float-right inflection-table flexbox " + "hintergrundfarbe2"
)
_FRAME_ADOC = """
[cols="1,1,1,1"]
|===
|Singular |Spelling |Singular |Spelling

{content}|===
"""


class Gender(Enum):
    """Enumeration for three German grammar genders."""

    M = "MASCULINE"
    F = "FEMININE"
    N = "NEUTER"


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


class Word:
    """Basic information for a particular word, no matter what the form.

    Because there is an independent ``wiktionary`` webpage for every
    word.
    """

    def __init__(self, spelling: str) -> None:
        """Init for a German word based on its spelling.

        Args:
            spelling: how the word is spelled. The spelling will be
                checked when initiating.
        """
        checked = check_de(spelling)

        #: str: how to spell.
        self.spelling = checked
        #: str: how to pronounce in International Phonetic Alphabet.
        self.ipa = None
        #: str: the ``Wiktionary`` link for it.
        self.link_wiki = _LINK_WIKI.format(word=self.spelling)
        # str: how to spell after syllabification.
        self.syllabification = None

        soup = self.crawl()
        self._assign_ipa(soup)
        self._assign_syllabification(soup)

    def crawl(self) -> BeautifulSoup:
        """Crawl the webpage of the conjugation from ``Wiktionary``.

        Returns:
            The crawled ``Wiktionary`` webpage.
        """
        source = requests.get(self.link_wiki).text
        soup = BeautifulSoup(source, "lxml")
        return soup

    def _assign_ipa(self, soup: BeautifulSoup):
        """Find IPA in crawled webpage.

        Args:
            soup: the crawled ``Wiktionary`` webpage.
        """
        #: str: how to pronounce in IPA without bracket.
        ipa = soup.find("span", class_="ipa").text
        self.ipa = f"[{ipa}]"

    def _assign_syllabification(self, soup: BeautifulSoup):
        """Find spelling after syllabification in crawled webpage.

        Note:
            The <p> tag with title "Worttrennung" is found first, and
            the syllabification is the first description list (tagged
            with "dl") following it.

        Args:
            soup: the crawled ``Wiktionary`` webpage.
        """
        tag = soup.find(
            "p", attrs=_ATTRS_SYLLABIFICATION
        ).next_element.next_element.next_element

        # Extra info in some webpage, which is not essential, so only
        # the str before the first comma is preserved.
        raw = tag.text.split(",")[0]
        if remove_cdot(raw) != self.spelling:
            logger.warning(
                f'The syllabification of "{self.spelling}", "{raw}", '
                "is not correct"
            )

        self.syllabification = raw


class Verb:
    """German verb."""

    def __init__(self, origin: str) -> None:
        """Init a German verb based on its original form.

        Args:
            origin: a German verb in its original form.
        """
        self.origin = origin
        self.link_reverso = _LINK_REVERSO.format(origin=self.origin)

        self.present = _PRESENT
        self.crawl_present()

    def crawl_present(self) -> None:
        """Crawl six present conjugations in ``conjugator.reverso.net``."""
        source = requests.get(self.link_reverso).text
        soup = BeautifulSoup(source, "lxml")
        conj = soup.find("div", class_="content-conj content-conj-inner")
        present = conj.find("div", class_="blue-box-wrap").find("ul")

        conjugations = present.find_all("li")
        for i in range(6):
            which = _PRESENT_LIST[i]
            spelling = conjugations[i].text.split(" ")[1]
            self.present[which] = VerbConjugation(which, spelling, self.origin)

    # def __str__(self) -> str:
    #     data = [
    #         self.present[i].info for i in _PRESENT_LIST
    #     ]
    #     return tabulate(data, headers=_HEADERS_PRESENT)

    def to_adoc(self) -> str:
        """Print present conjugations in Asciidoc-friendly format.

        Returns:
            Present conjugations in Asciidoc-friendly format.
        """
        content = ""
        for row in _PRESENT_LIST:
            content += f"{self.present[row]._info_adoc}\n"
        return _FRAME_ADOC.format(content=content)


class VerbConjugation(Word):
    """A conjugation of a verb in German."""

    def __init__(
        self, which: str, spelling: str, origin: Optional[str] = None
    ) -> None:
        """Init a conjugation for a German verb based on its form.

        Args:
            which: what kind of conjugation it is.
            spelling: how the conjugation looks like.
            origin: its original form.
        """
        #: str: what kind of conjugation it is.
        self.which = which
        #: str: the original form.
        self.origin = origin

        super().__init__(spelling)

    @property
    def info(self) -> Tuple[str, str, str]:
        """Info of the conjugation without its original form.

        Returns:
            The category, spelling, and IPA of the conjugation.
        """
        return (_PRINT_PRESENT[self.which], self.syllabification, self.ipa)

    @property
    def _info_adoc(self) -> str:
        """Print conjugation in as Asciidoc-table-row-friendly format.

        Returns:
            Conjugation in as Asciidoc-table-row-friendly format.
        """
        row = ""
        for cell in self.info:
            row += f"|{cell} "
        return row


class Noun(Word):
    """German noun."""

    def __init__(self, spelling: str) -> None:
        """Init for a German noun based on its spelling.

        Args:
            spelling: how the conjugation looks like.
        """
        super().__init__(spelling)

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

        res = _FRAME_ADOC.format(content=content)
        return res
