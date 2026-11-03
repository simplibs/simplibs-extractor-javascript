from typing import Final
from simplibs.extractor import Profile, by_suffix
# Outers
from ..constants import JS_SUFFIXES
from ..file_rules import JS_BASE, JS_STRICT_EXCLUDE
from ..presets import JS_CLEAN


JS_SRC_CLEAN: Final[Profile] = Profile(
    system="javascript",
    name="src-clean",
    description="Like code-clean, without tests, configuration, type declarations, assets and build folders",
    include=JS_BASE,
    exclude=JS_STRICT_EXCLUDE,
    steps=by_suffix(JS_CLEAN, JS_SUFFIXES),
    output_name="javascript_src_clean.md",
)
"""The profile `javascript/src-clean`."""


_DESIGN_NOTES = """
# JS_SRC_CLEAN — `javascript/src-clean`

## Purpose
The old strict React filter made visible: only the application's own source.

## Output
`javascript_src_clean.md`.
"""
