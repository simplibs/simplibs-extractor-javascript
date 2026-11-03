from .JS_CLEAN import JS_CLEAN
from .JS_NO_IMPORTS import JS_NO_IMPORTS


__all__ = [
    "JS_CLEAN",
    "JS_NO_IMPORTS",
]


_DESIGN_NOTES = """
# simplibs.extractor_javascript.presets — Ready-Made Pipeline Steps

## Purpose
Chains of actions that the profiles use, built once.

    from simplibs.extractor_javascript.presets import JS_CLEAN
    steps = JS_CLEAN

## Domain Folder
`presets/` has its own `__all__` and is not re-exported from the package root.
It stands to the right of `actions` (it uses them) and to the left of `profiles`.

## Internal Components Registry

| Component       | Type   | Description                                                      |
| :-------------- | :----- | :--------------------------------------------------------------- |
| `JS_CLEAN`      | Preset | JavaScript and TypeScript without comments, whitespace tidied.   |
| `JS_NO_IMPORTS` | Preset | JavaScript logic only, compact.                                  |
"""
