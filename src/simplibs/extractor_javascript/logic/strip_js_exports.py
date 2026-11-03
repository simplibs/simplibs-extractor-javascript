from simplibs.text import remove_spans
from simplibs.validate import validate_call
# Outers
from ..constants import (
    JS_EXPORT_DEFAULT_NAME_PATTERN,
    JS_EXPORT_KEYWORD_PATTERN,
    JS_EXPORT_LIST_PATTERN,
)
# Inners
from ._helpers import find_matches_outside, scan_js


@validate_call
def strip_js_exports(text: str) -> str:
    """Remove what only exports from a JavaScript or TypeScript source, and keep the code.

    Args:
        text: The source.

    Returns:
        The text without `export { ... }`, `export * from "m"` and `export default Name;`,
        and without the `export` / `export default` keyword in front of a named declaration.
        An anonymous `export default ...` stays.
    """

    # 1. One scan serves all three patterns: they never match the same line
    scan = scan_js(text)

    # 2. Lines that only export are cut whole
    spans = [
        match.span()
        for pattern in (JS_EXPORT_LIST_PATTERN, JS_EXPORT_DEFAULT_NAME_PATTERN)
        for match in find_matches_outside(text, pattern, scan)
    ]

    # 3. In front of a declaration only the keyword goes; the indentation (group 1) stays
    spans += [
        (match.end(1), match.end())
        for match in find_matches_outside(text, JS_EXPORT_KEYWORD_PATTERN, scan)
    ]

    return remove_spans(text, spans)


_DESIGN_NOTES = """
# strip_js_exports — Visibility Out, Code Kept

## Purpose
A step of the profile `javascript/code-no-imports`: `export` says who may use a
declaration, not what it does.

## Three Kinds of Export
1. Lists (`export { a, b }`, `export * from "m"`): hold no code, removed whole.
2. A default export of a name (`export default App;`): removed whole.
3. A declaration with `export` or `export default` in front: the keyword is
   removed and the declaration, indentation and all, stays.

## What Stays
`export default function () {}`, `export default () => {}` and
`export default class extends X {}` are anonymous: without the keyword they
would not be valid, so they are not touched.
"""
