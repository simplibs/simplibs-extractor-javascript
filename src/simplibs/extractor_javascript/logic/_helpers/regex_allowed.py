# Outers
from ...constants import JS_REGEX_KEYWORDS
# Inners
from .is_word_char import is_word_char


def regex_allowed(last: str, word: str, before_last: str = "", closing_tag: bool = False) -> bool:
    """Decide whether a `/` starts a regular expression (and is not a division).

    Args:
        last: The last character of the previous significant token (comments and blanks do not count).
        word: The identifier that token ended with, if any.
        before_last: The character before `last`.
        closing_tag: The slash is followed by what ends a JSX closing tag (`/div>`).

    Returns:
        `True` if the slash begins a regular expression literal.
    """

    # 1. `=> /re/` is a regex; a `>` that closes a type (`Array<T> / 2`) is not
    if last == ">":
        return before_last == "="

    # 2. After `<`: `</div>` opens a JSX closing tag, anything else (`n </x/.test(s)`) is a regex
    if last == "<":
        return not closing_tag

    # 3. Nothing before it, or an operator or opening bracket: an expression begins here
    if last == "" or last in "(,=:[!&|?{;+-*%~^":
        return True

    # 4. After a word it depends on the word
    if is_word_char(last):
        return word in JS_REGEX_KEYWORDS

    # 5. After `)`, `]`, `}`, a literal or another slash: a division
    return False


_DESIGN_NOTES = """
# regex_allowed — Division or Regular Expression

## Purpose
The one ambiguity of JavaScript that a scanner cannot avoid: `/` is both. A
regex literal may hold `//` or `/*` or a quote, and mistaking a division for
one would swallow the code that follows.

## How It Decides
By the last significant token before the slash, as a regex-aware tokenizer
does. A heuristic, not a parser: after `<` it asks whether a closing tag follows (`</div>` or a comparison with a regex), after `)` it says division (right for
`f(x) / 2`, wrong for `if (x) /re/.test(y)`), after `}` division (right for
the end of a JSX expression, wrong for a regex that starts a statement).

## Why These Mistakes Are Bearable
A slash taken for a division only means a regex literal is scanned as code:
a quote in it opens a "string" that ends at the end of the line. A slash
taken for a regex ends at the end of the line too. The damage never spreads
past one line.
"""
