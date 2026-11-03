from typing import Final
from simplibs.path.rules import AnyParentNameIs, NameIs
from simplibs.rules import IsIn, Regex, Rule
# Outers
from ...constants import JS_TEST_DIR_NAMES


JS_TESTS: Final[Rule] = (
    NameIs(Regex(r"(^|[._-])(test|spec)s?([._-]|$)"))
    | AnyParentNameIs(IsIn(JS_TEST_DIR_NAMES))
)
"""The file is a JavaScript test: by its name (`a.test.js`, `a.spec.ts`) or by its folder (`__tests__/`)."""


_DESIGN_NOTES = """
# JS_TESTS — A Test Is Named `test` or `spec` as a Whole Word

## Purpose
Part of the strict JavaScript exclusion.

## Why a Pattern
`test` or `spec` (with an optional `s`) must stand alone in the name:
at the start, or after `.`, `-`, `_`, and followed by one of them or by the
end. `App.test.tsx`, `a.spec.ts` and `test-utils.js` are tests; `latest.js`,
`contest.tsx` and `inspector.ts` are not.

## Or Inside a Test Folder
`__tests__`, `__mocks__`, `e2e`, `tests`, `test` and `coverage`.
"""
