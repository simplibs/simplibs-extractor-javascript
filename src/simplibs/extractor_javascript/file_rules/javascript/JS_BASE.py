from typing import Final
from simplibs.rules import Rule
# Inners
from .build_js_base import build_js_base


JS_BASE: Final[Rule] = build_js_base()
"""The default rule for JavaScript and TypeScript files worth reading: `index.*` and `_*` included."""


_DESIGN_NOTES = """
# JS_BASE — The Default Choice of JavaScript Files

## Purpose
`build_js_base()` with its defaults, built once. Every JavaScript profile of
this library uses it as `include`.
"""
