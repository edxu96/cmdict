"""A function for German word searching return based on several classes."""
from typing import Optional

from bs4 import BeautifulSoup
from loguru import logger
import requests

from cmdict.utils import remove_cdot

_ATTRS_SYLLABIFICATION = {"title": "Trennungsmöglichkeiten am Zeilenumbruch"}
_LINK_WIKI = "https://de.wiktionary.org/wiki/{word}"


class Word:
    """Basic information for a particular word, no matter what the form.

    Because there is an independent ``wiktionary`` webpage for every
    word.
    """

    def __init__(self, spelling: str) -> None:
        """Init for a German word based on its spelling.

        Note:
            The corresponding ``Wiktionary`` webpage is automatically
            crawled and parsed.

        Args:
            spelling: how the word is spelled. The spelling will be
                checked when initiating.
        """
        #: str: how to spell.
        self.spelling = spelling
        #: str: how to pronounce in International Phonetic Alphabet.
        self.ipa = ""
        #: str: the ``Wiktionary`` link for it.
        self.link_wiki = _LINK_WIKI.format(word=self.spelling)
        # str: how to spell after syllabification.
        self.syllabification = ""

        soup = self.crawl_wiktionary()
        self._assign_ipa(soup)
        self._assign_syllabification(soup)

    def crawl_wiktionary(self) -> BeautifulSoup:
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
        try:
            ipa = soup.find("span", class_="ipa").text
            self.ipa = f"[{ipa}]"
        except AttributeError:
            logger.critical(f"IPA for {self.spelling} is not found.")

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


class InflectedWordForm(Word):
    """Represent a inflected word for a German word."""

    def __init__(
        self,
        spelling: str,
        origin: Optional[str] = None,
    ) -> None:
        """Init an inflected word for mainly based on its spelling.

        Args:
            spelling: how the inflected word looks like.
            origin: its original form.
        """
        super().__init__(spelling)

        #: str: the original form.
        self.origin = origin
