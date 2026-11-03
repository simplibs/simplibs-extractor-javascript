import re
from typing import Final


JS_IMPORT_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"""^[ \t]*import(?:\s+(?!\()|(?=[{*"']))(?:(?:[^'";{]|\{[^}]*\})*?\bfrom\s*)?"""
    r"""(["'])[^"'\n]+\1[ \t]*(?:\s*;)?[ \t]*$""",
    re.MULTILINE,
)
"""A whole ES `import` statement on its own line(s): `import x from "m"`, `import {a} from "m"`, `import "m"`, `import type ...`."""


_DESIGN_NOTES = """
# JS_IMPORT_PATTERN — One Import Statement, the Whole Line

## Purpose
What `remove_js_imports` cuts out. The match starts at the beginning of the
line (with the indentation) and ends at the end of the statement, so the line
disappears whole.

## What It Takes
`import x from "m"`, `import { a, b as c } from "m"`, `import * as ns from "m"`,
`import "m"`, `import type { T } from "m"`, `import { "name" as x } from "m"` and
the same spread over several lines. A `;` on the line after the statement
belongs to it and goes with it.

## What It Leaves
A dynamic `import("m")` is an expression, not a statement: the `(` after
`import` is excluded. A statement that shares its line with other code or
a comment is left; comments are removed first in the profiles.
"""
