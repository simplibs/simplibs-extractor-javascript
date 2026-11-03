from simplibs.text import remove_spans
from simplibs.validate import validate_call
# Outers
from ..constants import JS_IMPORT_PATTERN
# Inners
from ._helpers import find_matches_outside, scan_js


@validate_call
def remove_js_imports(text: str) -> str:
    """Remove the ES `import` statements of a JavaScript or TypeScript source.

    Args:
        text: The source.

    Returns:
        The text without `import` statements (`import type` included); the lines they stood on disappear.
        A dynamic `import("m")` stays.
    """

    # 1. The statements that start in code
    matches = find_matches_outside(text, JS_IMPORT_PATTERN, scan_js(text))

    # 2. Each match is a whole line (or lines): cut it, the emptied line goes with it
    return remove_spans(text, [match.span() for match in matches])


_DESIGN_NOTES = """
# remove_js_imports — The Logic Without Its Dependencies

## Purpose
A step of the profile `javascript/code-no-imports`.

## By a Pattern, Not a Parser
An import is found by a line pattern; the scan only tells which matches are
real code. That is what makes it work for JSX and TypeScript with no parser
for either, and it is why a statement sharing its line with other code (a
minified bundle) is left.

## Needs No Order
Comments and strings are known to the scan, so the step gives the same
result before or after `strip_js_comments`; only an import followed by a comment
on the same line needs the comments gone first.
"""
