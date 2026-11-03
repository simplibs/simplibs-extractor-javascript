from typing import Final


JS_SEPARATORS: Final[str] = " \t\r\n{}()[],;"
"""Characters that already keep two JavaScript tokens apart."""


_DESIGN_NOTES = """
# JS_SEPARATORS — Where Two Tokens Cannot Grow Together

## Purpose
When a block comment is cut out from between two tokens (`a/**/b`), the
tokens must not touch afterwards: `ab` is a different name. A character from
this set on either side means they are separated anyway and nothing has to
be put in.
"""
