# Inners
from .is_word_char import is_word_char


def skip_regex(text: str, start: int) -> int:
    """Find where a regular expression literal ends, flags included.

    Args:
        text: The source.
        start: The offset of the opening `/`.

    Returns:
        The offset just after the flags; `start + 1` if the line ends before the closing
        slash, which means it was not a regular expression after all.
    """

    # 1. Walk to the closing slash; one inside a `[...]` class does not close it
    position = start + 1
    length = len(text)
    in_class = False
    while position < length:
        character = text[position]
        if character == "\\":
            position += 2
        elif character == "\n":
            return start + 1
        elif character == "[":
            in_class, position = True, position + 1
        elif character == "]":
            in_class, position = False, position + 1
        elif character == "/" and not in_class:

            # 2. The flags are a run of letters
            position += 1
            while position < length and is_word_char(text[position]):
                position += 1
            return position
        else:
            position += 1

    return length


_DESIGN_NOTES = """
# skip_regex — A Regular Expression, to Its Flags

## Purpose
`/[/*]/` and `/"/` hold characters that would open a comment or a string. The
scanner skips the literal whole.

## The Class
Inside `[...]` a slash is an ordinary character: `/[/]/` is one literal.

## Not a Regex After All
A regex literal ends on its line. If the line ends first, the slash was an
operator the heuristic took for a regex, and only that one character is
consumed, so scanning goes on with the rest of the line as code.
"""
