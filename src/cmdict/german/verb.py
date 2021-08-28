"""Classes for German verb."""
from typing import Optional, Tuple

from bs4 import BeautifulSoup
import requests

from cmdict.german.spelling import Word

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
_ADOC_VERB = """== {origin}

[cols="1,1,1"]
|===
|Personalpronomen |Spelling |IPA

{conjugations}|===
"""


class Verb(Word):
    """German verb."""

    def __init__(self, spelling: str) -> None:
        """Init a German verb based on its original form.

        Args:
            spelling: a German verb in its original form.
        """
        super().__init__(spelling)

        self.link_reverso = _LINK_REVERSO.format(origin=self.spelling)

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
            how = conjugations[i].text.split(" ")[1]
            self.present[which] = VerbConjugation(which, how, self.spelling)

    def to_adoc(self) -> str:
        """Print present conjugations in Asciidoc-friendly format.

        Returns:
            Present conjugations in Asciidoc-friendly format.
        """
        conjugations = ""
        for row in _PRESENT_LIST:
            conjugations += f"{self.present[row]._info_adoc}\n"

        origin = self.syllabification + " " + self.ipa

        res = _ADOC_VERB.format(conjugations=conjugations, origin=origin)
        return res


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
