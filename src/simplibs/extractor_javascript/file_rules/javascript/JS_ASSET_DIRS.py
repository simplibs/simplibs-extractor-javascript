from typing import Final
from simplibs.path.rules import AnyParentNameIs
from simplibs.rules import IsIn, Rule
# Outers
from ...constants import JS_ASSET_DIR_NAMES


JS_ASSET_DIRS: Final[Rule] = AnyParentNameIs(IsIn(JS_ASSET_DIR_NAMES))
"""The file lies inside a folder of files served as they are (`public`, `static`, `assets`)."""


_DESIGN_NOTES = """
# JS_ASSET_DIRS — Copied, Not Compiled

## Purpose
Part of the strict JavaScript exclusion. See `JS_ASSET_DIR_NAMES`.
"""
