import re
from typing import Final


JS_EXPORT_DEFAULT_NAME_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^[ \t]*export\s+default\s+[A-Za-z_$][\w$]*"
    r"(?:\s*;[ \t]*$|[ \t]*$(?!\s*" + r"[,.(\[`+\-*/%<>=&|?:]" + r"))",
    re.MULTILINE,
)
"""`export default Name;`: the default export of something declared elsewhere."""


_DESIGN_NOTES = """
# JS_EXPORT_DEFAULT_NAME_PATTERN — A Default Export That Only Points

## Purpose
`export default App;` at the end of a component file holds no code, only a
name. It is removed whole.

## A Name That Goes On
`export default FILE` followed by `? a : b` on the next line is a conditional
expression, not a name: a line that the next one continues is not taken.

## What Stays
`export default function App() {}` and `export default () => {}` carry code.
The first loses only its keywords (see `JS_EXPORT_KEYWORD_PATTERN`), the
second stays as it is: without `export default` it would not be valid.
"""
