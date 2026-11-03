from .atomic import (
    DEPENDENCY_DIRS,
    DOT_NAME,
    INDEX_NAME,
    OUTPUT_DIRS,
    UNDERSCORE_NAME,
    VCS_DIRS,
)
from .javascript import (
    JS_ASSET_DIRS,
    JS_BASE,
    JS_CONFIG,
    JS_FILES,
    JS_STRICT_EXCLUDE,
    JS_TESTS,
    build_js_base,
)


__all__ = [
    # atomic
    "DEPENDENCY_DIRS",
    "DOT_NAME",
    "INDEX_NAME",
    "OUTPUT_DIRS",
    "UNDERSCORE_NAME",
    "VCS_DIRS",
    # javascript
    "JS_ASSET_DIRS",
    "JS_BASE",
    "JS_CONFIG",
    "JS_FILES",
    "JS_STRICT_EXCLUDE",
    "JS_TESTS",
    "build_js_base",
]


_DESIGN_NOTES = """
# simplibs.extractor_javascript.file_rules — Which Files Are Worth Reading

## Purpose
Rules on the path of a file, relative to the source folder. The profiles use
them as `include` and `exclude`; they compose with `&`, `|` and `~`, so a
program can build its own selection from them:

    from simplibs.extractor_javascript.file_rules import JS_BASE, JS_TESTS
    only_tests = JS_BASE & JS_TESTS

## Domain Folder
`file_rules/` has its own `__all__` and is not re-exported from the package root.

## Internal Components Registry

| Component    | Type    | Description                                                        |
| :----------- | :------ | :----------------------------------------------------------------- |
| `atomic`     | Package | The shared pieces: dot names, index, underscore, VCS folders...    |
| `javascript` | Package | Rules for JavaScript and TypeScript projects.                      |

## Layering & Design
- `atomic` ← `javascript`.
- Every rule is built once, when the package is imported.
- A rule about the folders above a file is `AnyParentNameIs` of `simplibs-path`; a set of names is `IsIn` of `simplibs-rules`.
"""
