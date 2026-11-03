from .logic import (
    js_comment_spans,
    remove_js_imports,
    remove_js_requires,
    strip_js_comments,
    strip_js_exports,
)
from .plugin import register_all


__all__ = [
    # steps
    "js_comment_spans",
    "remove_js_imports",
    "remove_js_requires",
    "strip_js_comments",
    "strip_js_exports",
    # add-on of the extractor
    "register_all",
]


_DESIGN_NOTES = """
# simplibs-extractor-javascript — Package Root

## Purpose
The add-on that teaches `simplibs-extractor` about JavaScript and TypeScript
(React included): file rules for such projects, the steps that clean the
source (comments, imports, requires, exports) and four ready profiles.
Install it and the profiles are there:

    simplibs-extractor javascript src-clean my_project

## What the Root Exports
The steps as plain functions (`str -> str`) and `register_all` (the target of
the entry point `simplibs.extractor.plugins`):

    from simplibs.extractor_javascript import strip_js_comments, remove_js_imports

## What the Root Deliberately Does NOT Export
Four domain folders with their own `__all__`, imported through their domain:

    from simplibs.extractor_javascript.actions import StripJsComments
    from simplibs.extractor_javascript.file_rules import JS_BASE, build_js_base
    from simplibs.extractor_javascript.presets import JS_CLEAN
    from simplibs.extractor_javascript.profiles import JS_SRC_CLEAN

and the internals: `_helpers/` inside `logic`.

## Spans
The steps find ranges of characters as `simplibs.text.Span`. The type is not
defined here, it is taken from `simplibs-text`.

## Layering
`constants` ← `file_rules` ← `logic` ← `actions` ← `presets` ← `profiles` ← `plugin`.
Each layer imports only from the layers on its left; the root imports from the ones it exports.

## `__all__`
Defined here and in the domain folders (`actions`, `file_rules`, `presets`,
`profiles`) only; the layers inside them use plain imports.
"""
