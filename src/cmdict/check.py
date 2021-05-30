"""Functions to check German spelling."""
from loguru import logger
from spellchecker import SpellChecker

_CHECKER = SpellChecker(language="de")


def check_de(spelling: str) -> str:
    """Return a corrected German spelling if not.

    Args:
        spelling: some German spelling input by user.

    Note:
        - It seems that ``pyspellchecker``, the package used here, does
          not support capitalisation in German, like that for nouns.
        - Every char is turned to its lower case.

    Returns:
        The most likely German spelling corresponding to the input spelling.
    """
    spelling = spelling.lower()

    checked = _CHECKER.correction(spelling)
    if checked != spelling:
        logger.warning(
            f'The input "{spelling}" is most likely an incorrect German word. '
            f'"{checked}" is chosen as the final spelling.'
        )

        # Not execute if the logging level is high.
        if logger.level == "debug":
            candidates = _CHECKER.candidates(spelling)
            candidates.discard(checked)
            logger.debug(f"There are other candidates: {candidates}.")

    return checked
