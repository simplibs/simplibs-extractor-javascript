from typing import Final
from simplibs.extractor import Profile, by_suffix
# Outers
from ..constants import JS_SUFFIXES
from ..file_rules import JS_BASE
from ..presets import JS_CLEAN


JS_CODE_CLEAN: Final[Profile] = Profile(
    system="javascript",
    name="code-clean",
    description="JavaScript and TypeScript without comments and extra blank lines (imports and exports stay)",
    include=JS_BASE,
    steps=by_suffix(JS_CLEAN, JS_SUFFIXES),
    output_name="javascript_code_clean.md",
)
"""The profile `javascript/code-clean`."""


_DESIGN_NOTES = """
# JS_CODE_CLEAN — `javascript/code-clean`

## Purpose
The old `REACT_CODE_CLEAN`. JSDoc goes with the other comments.

## Output
`javascript_code_clean.md`. The step is chosen by file type, with the same
pipeline for all six JavaScript and TypeScript suffixes.
"""
