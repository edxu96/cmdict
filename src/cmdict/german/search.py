"""Function to gather information on a German word and return result."""
from typing import Union

from cmdict.check import check_de
from cmdict.german.noun import Noun
from cmdict.german.pos import crawl_pos_de, PartOfSpeechDe
from cmdict.german.verb import Verb

_SECRET = "556e44c4daf89fe1f32c661284dbabca2caac043e949ff4ead175af30732a15d"


def search_word_de(spelling: str) -> Union[str, None]:
    """Check spelling, detect PoS and get printout based on it class.

    Args:
        spelling: a spelling specified as German.

    Returns:
        Printout of search result or None if not supported.
    """
    word = check_de(spelling)
    if crawl_pos_de(word, _SECRET) == PartOfSpeechDe.Noun:
        res = Noun(word).to_adoc()
    elif crawl_pos_de(word, _SECRET) == PartOfSpeechDe.Verb:
        res = Verb(word).to_adoc()
    else:
        res = None
    return res
