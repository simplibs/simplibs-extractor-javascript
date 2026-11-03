import re
from typing import Final


JS_EXPORT_LIST_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"""^[ \t]*export\s*(?:type\s+)?(?:\*(?:\s+as\s+[\w$]+)?|\{[^}]*\})\s*"""
    r"""(?:from\s*(["'])[^"'\n]+\1)?[ \t]*(?:\s*;)?[ \t]*$""",
    re.MULTILINE,
)
"""An export that only names things: `export { a, b }`, `export * from "m"`, `export * as ns from "m"`, `export type { T }`."""


_DESIGN_NOTES = """
# JS_EXPORT_LIST_PATTERN — Exports That Hold No Code

## Purpose
`export { a, b }` and `export * from "./x"` declare nothing; they only say what
is visible from outside. For reading the code they are removed whole.
"""
