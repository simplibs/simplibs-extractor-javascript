from .RemoveJsImports import RemoveJsImports
from .RemoveJsRequires import RemoveJsRequires
from .StripJsComments import StripJsComments
from .StripJsExports import StripJsExports


__all__ = [
    "RemoveJsImports",
    "RemoveJsRequires",
    "StripJsComments",
    "StripJsExports",
]


_DESIGN_NOTES = """
# simplibs.extractor_javascript.actions — The Steps as Pipeline Actions

## Purpose
Every step of `logic/` as an `Action` of `simplibs-actions`, so it can be
chained with `>>` and used as the `steps` of an extractor profile.

    from simplibs.extractor_javascript.actions import StripJsComments, RemoveJsImports
    steps = StripJsComments() >> RemoveJsImports()

## Domain Folder
`actions/` has its own `__all__` and is not re-exported from the package root:
a function and an action are different kinds of thing and stay visibly
different at the import line.

## Thin Wrappers
Each action is `create_action(function, main_param="text", ...)`.

## Internal Components Registry

| Component          | Type   | Description                            |
| :----------------- | :----- | :------------------------------------- |
| `RemoveJsImports`  | Action | Over `remove_js_imports`.              |
| `RemoveJsRequires` | Action | Over `remove_js_requires`.             |
| `StripJsComments`  | Action | Over `strip_js_comments`.              |
| `StripJsExports`   | Action | Over `strip_js_exports`.               |
"""
