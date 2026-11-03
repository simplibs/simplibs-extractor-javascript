from typing import Final
from simplibs.path.rules import NameIs
from simplibs.rules import EndsWith, Rule
# Outers
from ..atomic import DEPENDENCY_DIRS, OUTPUT_DIRS, VCS_DIRS
# Inners
from .JS_ASSET_DIRS import JS_ASSET_DIRS
from .JS_CONFIG import JS_CONFIG
from .JS_TESTS import JS_TESTS


JS_STRICT_EXCLUDE: Final[Rule] = (
    JS_TESTS
    | JS_CONFIG
    | NameIs(EndsWith(".d.ts"))
    | VCS_DIRS
    | DEPENDENCY_DIRS
    | OUTPUT_DIRS
    | JS_ASSET_DIRS
)
"""Everything that is JavaScript-looking but not the application's own logic: tests, configuration, type declarations, assets, installed packages, build output."""


_DESIGN_NOTES = """
# JS_STRICT_EXCLUDE — Only What the Application Does

## Purpose
The `exclude` of the profile `javascript/src-clean`.

## Type Declarations
A `.d.ts` file only describes the types of code that exists elsewhere.

## Installed Packages
`node_modules` has its own rule here (`DEPENDENCY_DIRS`), because the library
no longer counts it among the version-control folders.
"""
