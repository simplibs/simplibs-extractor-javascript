from .JS_CODE_CLEAN import JS_CODE_CLEAN
from .JS_CODE_NO_IMPORTS import JS_CODE_NO_IMPORTS
from .JS_DATA_ALL import JS_DATA_ALL
from .JS_PROFILES import JS_PROFILES
from .JS_SRC_CLEAN import JS_SRC_CLEAN


__all__ = [
    "JS_CODE_CLEAN",
    "JS_CODE_NO_IMPORTS",
    "JS_DATA_ALL",
    "JS_PROFILES",
    "JS_SRC_CLEAN",
]


_DESIGN_NOTES = """
# simplibs.extractor_javascript.profiles — The Profiles Themselves

## Purpose
The four profiles as `Profile` objects of the extractor. Registering them is
the job of `register_all`; having them as objects lets a program use one
directly or build its own on top of it.

    from simplibs.extractor_javascript.profiles import JS_SRC_CLEAN
    from dataclasses import replace
    mine = replace(JS_SRC_CLEAN, name="mine", output_name="mine.md")

## Domain Folder
`profiles/` has its own `__all__` and is not re-exported from the package root.

## Internal Components Registry

| Component            | Type    | Description                                               |
| :------------------- | :------ | :-------------------------------------------------------- |
| `JS_CODE_CLEAN`      | Profile | `javascript/code-clean`: comments removed.                |
| `JS_CODE_NO_IMPORTS` | Profile | `javascript/code-no-imports`: the logic only.             |
| `JS_DATA_ALL`        | Profile | `javascript/data-all`: every file as it is.               |
| `JS_PROFILES`        | Tuple   | All four profiles, in the order the listings show them.   |
| `JS_SRC_CLEAN`       | Profile | `javascript/src-clean`: the application's own code, cleaned. |

## Layering & Design
- `by_suffix` (one step for a family of file types) is a tool of `simplibs-extractor`.
"""
