def is_word_char(character: str) -> bool:
    """Tell whether a character can be part of a JavaScript identifier or a number.

    Args:
        character: A single character.

    Returns:
        `True` for letters, digits (of any script), `_` and `$`.
    """

    # 1. What an identifier is made of
    return character.isalnum() or character in "_$"


_DESIGN_NOTES = """
# is_word_char — One Character of a Name

## Purpose
The scanner follows words (to know that `return` came before a slash) and the
flags of a regular expression (`/x/gi`). Both are runs of these characters.

## Any Script
`str.isalnum` is true for `é` and `ž` as well, so identifiers in any language
are followed correctly.
"""
