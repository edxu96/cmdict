"""Functions to check German spelling."""
from loguru import logger
from spellchecker import SpellChecker

_CHECKER = SpellChecker(language="de")


def check_de(word: str) -> str:
    """Return a corrected German spelling if not.

    Args:
        word: some German word input by user.

    Note:
        It seems that ``pyspellchecker``, the package used here, does
        not support capitalisation in German, like that for nouns.

    Returns:
        The most likely German word corresponding to the input spelling.
    """
    checked = _CHECKER.correction(word)
    if checked != word:
        logger.warning(
            f'The input "{word}" is most likely an incorrect German word. '
            f'"{checked}" is chosen as the final spelling.'
        )

        # Not execute if the logging level is high.
        if logger.level == "debug":
            candidates = _CHECKER.candidates(word)
            candidates.discard(checked)
            logger.debug(f"There are other candidates: {candidates}.")

    return checked
