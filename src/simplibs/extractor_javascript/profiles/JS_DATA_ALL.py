from typing import Final
from simplibs.extractor import Profile
# Outers
from ..file_rules import JS_BASE


JS_DATA_ALL: Final[Profile] = Profile(
    system="javascript",
    name="data-all",
    description="Every relevant JavaScript and TypeScript file, as it is",
    include=JS_BASE,
    output_name="javascript_data_all.md",
)
"""The profile `javascript/data-all`."""


_DESIGN_NOTES = """
# JS_DATA_ALL — `javascript/data-all`

## Purpose
The old `REACT_DATA_ALL`: the files selected by `JS_BASE`, untouched.

## Output
`javascript_data_all.md`.
"""
