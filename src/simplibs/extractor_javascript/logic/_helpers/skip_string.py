def skip_string(text: str, start: int) -> int:
    """Find where a quoted string literal ends.

    Args:
        text: The source.
        start: The offset of the opening quote (`'` or `"`).

    Returns:
        The offset just after the closing quote; for a string that is not closed,
        the end of its line.
    """

    # 1. Walk to the matching quote; a backslash takes the next character with it
    quote = text[start]
    position = start + 1
    length = len(text)
    while position < length:
        character = text[position]
        if character == "\\":
            position += 2
        elif character == quote:
            return position + 1
        elif character == "\n":
            return position
        else:
            position += 1

    return length


_DESIGN_NOTES = """
# skip_string — A String Ends at Its Quote or at Its Line

## Purpose
A `//` or `/*` inside a string is text, not a comment. The scanner skips the
whole string so it never looks inside.

## An Unterminated String
A single or double quoted string cannot span lines in JavaScript, so a quote
that is not closed on its line is not a string (an apostrophe in JSX text, say:
`<p>Don't</p>`). Scanning stops at the end of the line and the error stays
on that one line.

## Escapes
A backslash takes the next character, so `'it\\'s'` and a line continuation
(`\\` at the end of a line) are both one string.
"""
