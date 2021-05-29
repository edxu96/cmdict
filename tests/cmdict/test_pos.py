"""Test function to determine part of speech for a word."""
from cmdict.pos import crawl_pos_de, PartOfSpeechDe

SECRET = "556e44c4daf89fe1f32c661284dbabca2caac043e949ff4ead175af30732a15d"


def test_crawl_pos_de_pons():
    """Test crawl PoS for a German word in ``api.pons.com``."""
    assert crawl_pos_de("Schlafen", SECRET) == PartOfSpeechDe.Verb
    assert crawl_pos_de("schlafen", SECRET) == PartOfSpeechDe.Verb

    assert crawl_pos_de("Hilfe", SECRET) == PartOfSpeechDe.Noun
    assert crawl_pos_de("hilfe", SECRET) == PartOfSpeechDe.Noun

    assert crawl_pos_de("schön", SECRET) is None
