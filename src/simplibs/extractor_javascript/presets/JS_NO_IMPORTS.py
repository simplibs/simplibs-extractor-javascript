from typing import Final
from simplibs.text.presets import COMPACT
# Outers
from ..actions import RemoveJsImports, RemoveJsRequires, StripJsComments, StripJsExports


JS_NO_IMPORTS: Final = (
    StripJsComments()
    >> RemoveJsImports()
    >> RemoveJsRequires()
    >> StripJsExports()
    >> COMPACT
)
"""JavaScript and TypeScript reduced to their logic: no comments, imports, requires or exports, and no blank lines."""


_DESIGN_NOTES = """
# JS_NO_IMPORTS — The Logic and Nothing Else

## Purpose
The steps of `javascript/code-no-imports`.

## Order
Comments go first: an import followed by a comment on the same line is only
a whole line once the comment is gone.
"""
