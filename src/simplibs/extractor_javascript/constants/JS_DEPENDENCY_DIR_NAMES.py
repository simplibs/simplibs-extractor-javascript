from typing import Final


JS_DEPENDENCY_DIR_NAMES: Final[tuple[str, ...]] = ("node_modules",)
"""Names of folders that hold installed packages of a JavaScript project."""


_DESIGN_NOTES = """
# JS_DEPENDENCY_DIR_NAMES — Other People's Code

## Purpose
The names behind `DEPENDENCY_DIRS`. `node_modules` holds tens of thousands of
files that are not the project.

## Why Its Own Constant
The old code listed `node_modules` among the version-control folders. It is
not version control, and version control now comes from `simplibs-path`.
"""
