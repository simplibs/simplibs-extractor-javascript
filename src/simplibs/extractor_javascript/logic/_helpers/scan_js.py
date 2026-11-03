from simplibs.text.annotations import Span
# Outers
from ...constants import JS_CLOSING_TAG, JS_SEPARATORS
# Inners
from .JsScan import JsScan
from .is_word_char import is_word_char
from .regex_allowed import regex_allowed
from .skip_regex import skip_regex
from .skip_string import skip_string
from .skip_template import skip_template


def scan_js(text: str) -> JsScan:
    """Read a JavaScript or TypeScript source once and find its comments and literals.

    Args:
        text: The source.

    Returns:
        The comments, the comments that need a space left behind and the string and template literals.
    """

    # 1. State: where we are, and the last significant token (comments and blanks do not count)
    length = len(text)
    position = 0
    comments: list[Span] = []
    glued: list[Span] = []
    literals: list[Span] = []
    last = before_last = word = ""
    in_word = False

    while position < length:
        character = text[position]

        # 2. Blanks
        if character in " \t\r\n":
            position += 1
            in_word = False

        # 3. A string
        elif character in "'\"":
            end = skip_string(text, position)
            literals.append((position, end))
            position, before_last, last, word, in_word = end, last, '"', "", False

        # 4. A template literal
        elif character == "`":
            end = skip_template(text, position)
            literals.append((position, end))
            position, before_last, last, word, in_word = end, last, "`", "", False

        # 5. Anything but a slash: follow the word it belongs to
        elif character != "/":
            word = (word + character if in_word else character) if is_word_char(character) else ""
            in_word = is_word_char(character)
            before_last, last, position = last, character, position + 1

        # 6. `//`: a comment to the end of the line, unless it follows a colon (`http://` in JSX text)
        elif text.startswith("//", position):
            if position > 0 and text[position - 1] == ":":
                position, before_last, last, word, in_word = position + 2, last, "/", "", False
                continue
            newline = text.find("\n", position)
            end = length if newline == -1 else newline
            start = position
            while start > 0 and text[start - 1] in " \t":
                start -= 1
            comments.append((start, end))
            position, in_word = end, False

        # 7. `/* ... */`
        elif text.startswith("/*", position):
            close = text.find("*/", position + 2)
            end = length if close == -1 else close + 2
            start = position
            after = text[end] if end < length else "\n"
            before = text[start - 1] if start > 0 else "\n"
            if after in " \t\r\n":
                while start > 0 and text[start - 1] in " \t":
                    start -= 1
                comments.append((start, end))
            elif before not in JS_SEPARATORS and after not in JS_SEPARATORS:
                comments.append((start, end))
                glued.append((start, end))
            else:
                comments.append((start, end))
            position, in_word = end, False

        # 8. A regular expression, or a division
        elif regex_allowed(last, word, before_last, closing_tag=JS_CLOSING_TAG.match(text, position) is not None):
            position, before_last, last, word, in_word = skip_regex(text, position), last, "x", "", False
        else:
            position, before_last, last, word, in_word = position + 1, last, "/", "", False

    return JsScan(tuple(comments), tuple(glued), tuple(literals))


_DESIGN_NOTES = """
# scan_js — A Scanner, Not a Regex Over the Whole Text

## Purpose
Everything the JavaScript steps need to know about a source comes from this
one pass: it knows strings, template literals and regular expressions, so a
`//` in a URL string or a `/*` in a regex is never taken for a comment.

## Not a Parser
It does not build a tree. It follows only what decides where a comment or a
literal begins: quotes, backticks, slashes and the last significant token
before a slash. That is why it cannot fail: there is no syntax it refuses.

## Errors Stay on One Line
A string that is not closed ends at its line, a regex that is not closed is
dropped at its line. The worst a surprising source can do is spoil the line it
is on.

## The `//` After a Colon
`http://example.com` in JSX text (outside any string) is not a comment. A
`//` right after `:` is therefore two slashes. The price: `case 1://note`
keeps its comment.

## A Block Comment Between Two Tokens
`a/**/b` must not become `ab`. A comment with no separator on either side is
reported in `glued`, and the step leaves a single space in its place.
"""
