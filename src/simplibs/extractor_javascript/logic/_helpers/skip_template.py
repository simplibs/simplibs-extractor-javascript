# Outers
from ...constants import JS_CLOSING_TAG
# Inners
from .is_word_char import is_word_char
from .regex_allowed import regex_allowed
from .skip_regex import skip_regex
from .skip_string import skip_string


def _skip_braces(text: str, start: int) -> int:
    """Find the `}` that closes a `${` of a template literal; the offset is just after the `${`."""

    # 1. State: the brace depth and the last significant token, to tell a division from a regex
    depth = 1
    position = start
    length = len(text)
    last = before_last = word = ""
    in_word = False

    while position < length:
        character = text[position]

        # 2. Blanks
        if character in " \t\r\n":
            position += 1
            in_word = False

        # 3. Strings and nested templates are skipped whole
        elif character in "'\"":
            position = skip_string(text, position)
            before_last, last, word, in_word = last, '"', "", False
        elif character == "`":
            position = skip_template(text, position)
            before_last, last, word, in_word = last, "`", "", False

        # 4. Comments are skipped
        elif text.startswith("//", position):
            newline = text.find("\n", position)
            position = length if newline == -1 else newline
        elif text.startswith("/*", position):
            close = text.find("*/", position + 2)
            position = length if close == -1 else close + 2

        # 5. A slash: a regular expression (it may hold quotes and braces) or a division
        elif character == "/":
            if regex_allowed(last, word, before_last, closing_tag=JS_CLOSING_TAG.match(text, position) is not None):
                position = skip_regex(text, position)
                before_last, last, word, in_word = last, "x", "", False
            else:
                position += 1
                before_last, last, word, in_word = last, "/", "", False

        # 6. Everything else; the braces are counted
        else:
            if character == "{":
                depth += 1
            elif character == "}":
                depth -= 1
                if depth == 0:
                    return position + 1
            word = (word + character if in_word else character) if is_word_char(character) else ""
            in_word = is_word_char(character)
            before_last, last, position = last, character, position + 1

    return length


def skip_template(text: str, start: int) -> int:
    """Find where a template literal ends, expressions included.

    Args:
        text: The source.
        start: The offset of the opening backtick.

    Returns:
        The offset just after the closing backtick; the end of the text if it is not closed.
    """

    # 1. Walk to the closing backtick; a `${` opens an expression that may hold anything
    position = start + 1
    length = len(text)
    while position < length:
        character = text[position]
        if character == "\\":
            position += 2
        elif character == "`":
            return position + 1
        elif character == "$" and text.startswith("{", position + 1):
            position = _skip_braces(text, position + 2)
        else:
            position += 1

    return length


_DESIGN_NOTES = """
# skip_template — A Template Literal Can Hold Code

## Purpose
`` `a // ${ "}" + `inner` } c` `` is one literal. A comment marker in its text is
text; the code in `${...}` may hold strings, braces, comments, regular
expressions and further templates, all of which must be skipped as what they
are.

## Regular Expressions Inside `${ }`
`${ s.replace(/'|"/g, "") }` holds a regex with quotes in it. Taken for code,
the first quote would open a "string" and the braces would be counted wrongly,
and the rest of the file would be taken for the inside of the template. The
expression is therefore followed with the same last-token rule the scanner
uses for a slash.

## Why Two Functions in One File
A template contains expressions, and an expression may contain a template:
the two call each other. Two files would import each other. One file keeps
the loop closed, with the private `_skip_braces` beside the public function.

## Multi-Line Is Fine
Unlike a quoted string, a template literal may span lines, so an unclosed one
runs to the end of the text.
"""
