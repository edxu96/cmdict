"""German articles."""
from enum import Enum

from cmdict.german.spelling import InflectedWordForm


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
    X = "not considered"


class Case(Enum):
    """Enumeration for four cases of an (inflected) German noun."""

    N = "norminativ"
    G = "gernitiv"
    D = "dativ"
    A = "akkusativ"


class DeclensionMethod(Enum):
    """Enumeration for eight ways to inflect a German noun."""

    NS = (Case.N, True)  # "Norminativ Singular"
    NP = (Case.N, False)  # "Norminativ Plural"
    GS = (Case.G, True)  # "Gernitiv Singular"
    GP = (Case.G, False)  # "Gernitiv Plural"
    DS = (Case.D, True)  # "Dativ Singuler"
    DP = (Case.D, False)  # "Dativ Plural"
    AS = (Case.A, True)  # "Akkusativ Singuler"
    AP = (Case.A, False)  # "Akkusativ Plural"


class Declension(InflectedWordForm):
    """Represent declension (origin) of a German noun/article."""

    def __init__(
        self,
        spelling: str,
        origin: str,
        singular: bool,
        gender: Gender,
        case: Case,
    ) -> None:
        """Init based on attributes.

        Args:
            spelling: how this inflected word is spelled.
            origin: the original word form of this word. None if this
                word form is the origin.
            singular: whether this word is singular.
            case: which case this word represents.
            gender: which grammatical gender this word belongs to.
        """
        super().__init__(spelling, origin=origin)

        self.singular = singular
        self.gender = gender
        self.case = case

    @classmethod
    def from_method(
        cls,
        spelling: str,
        origin: str,
        declension: DeclensionMethod,
        gender: Gender,
    ):
        """Init a declension based on basic info and declension method.

        Args:
            spelling: how the declension is spelled.
            origin: how the original form is spelled.
            declension: which declension method is used.
            gender: which gender this word form belongs to.

        Returns:
            An object storing detailed declension method, IPA, and
            syllabification.
        """
        return cls(
            spelling=spelling,
            origin=origin,
            singular=declension.value[1],
            gender=gender,
            case=declension.value[0],
        )


#: List[Tuple[str, bool, Gender, Case]]: spelling and features of 16
#:     German articles.
_ARTICLES_DEF = [
    ("der", True, Gender.M, Case.N),
    ("die", True, Gender.F, Case.N),
    ("das", True, Gender.N, Case.N),
    ("die", False, Gender.X, Case.N),
    ("den", True, Gender.M, Case.A),
    ("die", True, Gender.F, Case.A),
    ("das", True, Gender.N, Case.A),
    ("die", False, Gender.X, Case.A),
    ("des", True, Gender.M, Case.G),
    ("der", True, Gender.F, Case.G),
    ("des", True, Gender.N, Case.G),
    ("der", False, Gender.X, Case.G),
    ("dem", True, Gender.M, Case.D),
    ("der", True, Gender.F, Case.D),
    ("dem", True, Gender.N, Case.D),
    ("den", False, Gender.X, Case.D),
]
#: Dict[Tuple[bool, Gender, Case], Declension]: 16 German articles keyed
#:     by their three features.
ARTICLES_DEF = {
    (item[1], item[2], item[3]): Declension(
        item[0], None, item[1], item[2], item[3]
    )
    for item in _ARTICLES_DEF
}
#: List[Tuple[str, bool, Gender, Case]]: spelling and features of 16
#:     German articles.
_ARTICLES_INDEF = [
    ("ein", True, Gender.M, Case.N),
    ("eine", True, Gender.F, Case.N),
    ("ein", True, Gender.N, Case.N),
    ("einen", True, Gender.M, Case.A),
    ("eine", True, Gender.F, Case.A),
    ("ein", True, Gender.N, Case.A),
    ("eines", True, Gender.M, Case.G),
    ("einer", True, Gender.F, Case.G),
    ("eines", True, Gender.N, Case.G),
    ("einem", True, Gender.M, Case.D),
    ("einer", True, Gender.F, Case.D),
    ("einem", True, Gender.N, Case.D),
]
ARTICLES_INDEF = {
    (item[1], item[2], item[3]): Declension(
        item[0], None, item[1], item[2], item[3]
    )
    for item in _ARTICLES_INDEF
}
