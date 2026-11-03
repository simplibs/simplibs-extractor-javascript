from typing import Final


JS_OUTPUT_DIR_NAMES: Final[tuple[str, ...]] = ("build", "dist", "out", ".next")
"""Names of folders that hold generated build output of a JavaScript project."""


_DESIGN_NOTES = """
# JS_OUTPUT_DIR_NAMES — Generated, Not Written

## Purpose
The names behind `OUTPUT_DIRS`. Build output repeats the source in another
shape; reading it twice only costs tokens.

## `.next`
The build folder of Next.js. It starts with a dot, but `build_js_base()` only
leaves out dot FILES, so without this name the compiled pages inside would be
read as source.

## Own List
The library keeps its own list instead of borrowing one: what counts as
build output differs from language to language, and each add-on decides it
for its own language.
"""
