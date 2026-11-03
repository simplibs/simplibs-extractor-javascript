from simplibs.rules import Rule
from simplibs.validate import validate_call
# Outers
from ..atomic import DOT_NAME, INDEX_NAME, UNDERSCORE_NAME
# Inners
from .JS_FILES import JS_FILES


@validate_call
def build_js_base(*, include_index: bool = True, include_underscore: bool = True) -> Rule:
    """Build the rule that picks the JavaScript and TypeScript files worth reading.

    Args:
        include_index: Take `index.*` files. Switch off to leave out the files that only re-export.
        include_underscore: Take files whose name starts with `_` (`_app.tsx`). Switch off for private helpers only.

    Returns:
        A rule on the path relative to the source folder.
    """

    # 1. The core: JavaScript and TypeScript files that are not hidden
    rule = JS_FILES & ~DOT_NAME

    # 2. The two kinds the old code always dropped, unless asked to leave them out
    if not include_underscore:
        rule = rule & ~UNDERSCORE_NAME
    if not include_index:
        rule = rule & ~INDEX_NAME

    return rule


_DESIGN_NOTES = """
# build_js_base — Which JavaScript Files Are Source

## Purpose
The `include` of every JavaScript profile, with two switches.

## What Changed From the Old `ReactBase`
The old rule dropped every `index.*` and every `_*` file. In a real project
that loses the root `index.js` (the entry of the application) and Next.js
`pages/_app.tsx`. Both are taken by default now; the switches bring back the
old behaviour.

## Why the Name Starts With `build_`
The constant `JS_BASE` has its own file. On Windows and macOS two files whose
names differ only by case (`js_base.py`, `JS_BASE.py`) are the same file, so
the function got a name that differs by more than the case.
"""
