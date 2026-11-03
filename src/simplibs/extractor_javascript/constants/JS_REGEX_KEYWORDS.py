from typing import Final


JS_REGEX_KEYWORDS: Final[frozenset[str]] = frozenset({
    "return", "typeof", "case", "do", "else", "in", "of", "void",
    "delete", "throw", "new", "yield", "await", "instanceof",
})
"""JavaScript words after which a `/` starts a regular expression and not a division."""


_DESIGN_NOTES = """
# JS_REGEX_KEYWORDS — Is This Slash a Division?

## Purpose
`a / b` divides and `return /b/.test(x)` starts a regular expression, and the
only difference is what stands in front of the slash. After a word, it is
this list that decides: after `return`, `typeof`, `case`... an expression
begins, so a slash is a regex; after any other word (a variable, a number)
it is a division.

## Used By
`regex_allowed`, the decision inside the JavaScript scanner.
"""
