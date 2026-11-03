from typing import Final
from simplibs.extractor import Profile
# Inners
from .JS_CODE_CLEAN import JS_CODE_CLEAN
from .JS_CODE_NO_IMPORTS import JS_CODE_NO_IMPORTS
from .JS_DATA_ALL import JS_DATA_ALL
from .JS_SRC_CLEAN import JS_SRC_CLEAN


JS_PROFILES: Final[tuple[Profile, ...]] = (
    JS_CODE_CLEAN,
    JS_CODE_NO_IMPORTS,
    JS_DATA_ALL,
    JS_SRC_CLEAN,
)
"""The profiles of the system `javascript`."""


_DESIGN_NOTES = """
# JS_PROFILES — The `javascript` System

## Purpose
The profiles of one system in the order the listing commands show them.
"""
