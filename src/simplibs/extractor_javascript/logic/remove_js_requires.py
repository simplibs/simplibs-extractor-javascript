from simplibs.text import remove_spans
from simplibs.validate import validate_call
# Outers
from ..constants import JS_REQUIRE_PATTERN
# Inners
from ._helpers import find_matches_outside, scan_js


@validate_call
def remove_js_requires(text: str) -> str:
    """Remove the CommonJS `const x = require("m")` statements of a JavaScript source.

    Args:
        text: The source.

    Returns:
        The text without them; the lines they stood on disappear.
    """

    # 1. The statements that start in code
    matches = find_matches_outside(text, JS_REQUIRE_PATTERN, scan_js(text))

    # 2. Cut each whole line
    return remove_spans(text, [match.span() for match in matches])


_DESIGN_NOTES = """
# remove_js_requires — The CommonJS Counterpart of the Import Step

## Purpose
A step of the profile `javascript/code-no-imports`, for the files that never moved
to `import`.

## What Stays
`require(name)` with a variable, a declaration with several declarators and a
`require` in the middle of an expression are code and stay.
"""
