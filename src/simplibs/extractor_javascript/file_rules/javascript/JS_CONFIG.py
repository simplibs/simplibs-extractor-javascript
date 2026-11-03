from typing import Final
from simplibs.path.rules import NameIs
from simplibs.rules import IsIn, Rule
# Outers
from ...constants import JS_CONFIG_NAMES


JS_CONFIG: Final[Rule] = NameIs(IsIn(JS_CONFIG_NAMES))
"""The file is JavaScript tooling configuration (`package.json`, `tsconfig.json`, `vite.config.ts`...)."""


_DESIGN_NOTES = """
# JS_CONFIG — Tooling, Not Components

## Purpose
Part of the strict JavaScript exclusion. See `JS_CONFIG_NAMES`.
"""
