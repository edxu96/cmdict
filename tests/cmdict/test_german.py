"""Test classes for German verbs and nouns."""
from cmdict.german import search_word_de
from cmdict.german.article import ARTICLES_DEF, Case, Gender
from cmdict.german.noun import Noun
from cmdict.german.verb import Verb, VerbConjugation

NOUN = {"Kind"}


def test_verb():
    """Print present conjugations of ``schlafen`` using ``tabulate``."""
    v = Verb("schlafen")
    print(v.present)
    print(v)


def test_conjugation():
    """Check if single conjugation can be crawled correctly."""
    assert VerbConjugation("ich", "schlafe").info == (
        "ich",
        "schla·fe",
        "[ˈʃlaːfə]",
    )
    assert VerbConjugation("er", "schläft").info == (
        "er/sie/es",
        "schläft",
        "[ʃlɛːft]",
    )
    assert VerbConjugation("er", "buchstabiert").info == (
        "er/sie/es",
        "buch·sta·biert",
        "[ˌbuːxʃtaˈbiːɐ̯t]",
    )


def test_verb_adoc():
    """Print present conjugations of ``schlafen`` in Asciidoc format."""
    v = Verb("schlafen")
    print(v.to_adoc())


def test_noun_kid():
    """Check object for noun, "Kind"."""
    obj = Noun("Kind")
    assert obj.gender == Gender.N, '"Kind" is a neuter noun.'
    assert obj.singular, '"Kind" is singular.'
    assert (
        obj.article_def == ARTICLES_DEF[(True, Gender.N, Case.N)]
    ), 'Definite article for "Kind".'
    assert (
        obj.article_def.spelling == "das"
    ), 'Definite article for "Kind" is "das".'


def test_noun_football():
    """Check object for noun, "Fußball"."""
    obj = Noun("Fußball")
    assert obj.gender == Gender.M, '"Fußball" should be a masculine noun.'
    assert (
        obj.article_def == ARTICLES_DEF[(True, Gender.M, Case.N)]
    ), 'Definite article for "Kind".'
    assert (
        obj.article_def.spelling == "der"
    ), 'Definite article for "Kind" is "der".'


def test_search_word_de():
    """Check if a spelling can be corrected and its PoS is detected."""
    assert "Personalpronomen" in search_word_de("schlafen")
    assert "Singular" in search_word_de("Kind")
