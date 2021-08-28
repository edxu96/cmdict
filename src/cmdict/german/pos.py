"""Function to determine part of speech for a word using pons API.

Note:
    - ``l`` may yield results in both German-English and English-German
      directions.
    - ``in`` specifies the source language.
    - Read more about pons API in
      https://en.pons.com/p/files/uploads/pons/api/api-documentation.pdf
"""
from enum import Enum
from typing import Union

from loguru import logger
import requests

URL_API = "https://api.pons.com/v1/dictionary?l=deen&in=de&q={word}"


class PartOfSpeechDe(Enum):
    """Enumeration for part of speech in German.

    Note:
        Read more about part of speech in German (Wortart) in
        https://www.duden.de/hilfe/wortart.
    """

    Verb = "verb"
    Noun = "noun"
    Adv = "adverb"
    Adj = "adjective"


def crawl_pos_de(word: str, id_api: str) -> Union[PartOfSpeechDe, None]:
    """Crawl part of speech for a German word in ``api.pons.com``.

    Args:
        word: a German word, whose spelling should have been checked.
        id_api: API ID displayed in ``api.pons.com`` registration.

    Note:
        - Not sure if the implementation is robust enough, because there
          are multiple entries in the request from ``api.pons.com``, the
          first of which is primarily used.
        - Two kinds of PoS, verb and noun, are focused for now.
        - Read more about the API in
          https://en.pons.com/p/files/uploads/pons/api/api-documentation.pdf

    Returns:
        Part of speech for the German word.
    """
    crawled = requests.get(
        url=URL_API.format(word=word), headers={"X-Secret": id_api}
    )

    if crawled.status_code == 200:
        pos_raw = crawled.json()[0]["hits"][0]["roms"][0]["wordclass"]
        pos_raw_list = pos_raw.split(" ")

        if PartOfSpeechDe.Verb.value in pos_raw_list:
            pos = PartOfSpeechDe.Verb
        elif PartOfSpeechDe.Noun.value in pos_raw_list:
            pos = PartOfSpeechDe.Noun
        else:
            pos = None
            logger.warning(
                f'Part of speech for German spelling, "{word}", is unknown.'
            )
    else:
        logger.error(f'Incorrect request to "api.pons.com" for {word}.')
        pos = None
    return pos
