from typing import Final
from simplibs.path.rules import AnyParentNameIs
from simplibs.rules import IsIn, Rule
# Outers
from ...constants import JS_DEPENDENCY_DIR_NAMES


DEPENDENCY_DIRS: Final[Rule] = AnyParentNameIs(IsIn(JS_DEPENDENCY_DIR_NAMES))
"""The file lies inside a folder of installed packages (`node_modules`)."""


_DESIGN_NOTES = """
# DEPENDENCY_DIRS — Other People's Code

## Purpose
Part of the strict JavaScript exclusion. See `JS_DEPENDENCY_DIR_NAMES`.
"""
