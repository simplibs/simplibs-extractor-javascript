from typing import Final


JS_TEST_DIR_NAMES: Final[tuple[str, ...]] = ("__tests__", "__mocks__", "e2e", "tests", "test", "coverage")
"""Names of folders that hold JavaScript and TypeScript tests, mocks and coverage reports."""


_DESIGN_NOTES = """
# JS_TEST_DIR_NAMES — Where JavaScript Tests Live

## Purpose
Used by `JS_TESTS`. `coverage` is not a test, but it is generated from them
and has no place in a reading of the source.
"""
