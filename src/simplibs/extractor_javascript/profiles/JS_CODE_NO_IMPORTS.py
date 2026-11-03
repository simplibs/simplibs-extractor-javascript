from typing import Final
from simplibs.extractor import Profile, by_suffix
# Outers
from ..constants import JS_SUFFIXES
from ..file_rules import JS_BASE
from ..presets import JS_NO_IMPORTS


JS_CODE_NO_IMPORTS: Final[Profile] = Profile(
    system="javascript",
    name="code-no-imports",
    description="Pure logic: no imports, requires, exports, comments or blank lines",
    include=JS_BASE,
    steps=by_suffix(JS_NO_IMPORTS, JS_SUFFIXES),
    output_name="javascript_code_no_imports.md",
)
"""The profile `javascript/code-no-imports`."""


_DESIGN_NOTES = """
# JS_CODE_NO_IMPORTS — `javascript/code-no-imports`

## Purpose
The old `REACT_CODE_CLEAN_NO_IMPORTS`.

## Output
`javascript_code_no_imports.md`.
"""
