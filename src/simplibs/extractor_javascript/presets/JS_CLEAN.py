from typing import Final
from simplibs.text.presets import CLEANUP_WHITESPACE
# Outers
from ..actions import StripJsComments


JS_CLEAN: Final = (
    StripJsComments()
    >> CLEANUP_WHITESPACE
)
"""JavaScript and TypeScript without comments, whitespace tidied: imports and exports stay."""


_DESIGN_NOTES = """
# JS_CLEAN — The Everyday Clean Read

## Purpose
The steps of `javascript/code-clean` and `javascript/src-clean` as one object, built once.
"""
