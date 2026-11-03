from typing import Final


JS_SUFFIXES: Final[tuple[str, ...]] = (".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs")
"""The suffixes of JavaScript and TypeScript source files."""


_DESIGN_NOTES = """
# JS_SUFFIXES — What Counts as JavaScript or TypeScript

## Purpose
The JavaScript rules choose files by these suffixes and the JavaScript
profiles choose the steps by them (the extractor gives a step the text only,
never the path).

## `.mjs` and `.cjs`
ES modules and CommonJS files with an explicit module type. The old code did
not know them.
"""
