import re
from typing import Final


JS_REQUIRE_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"""^[ \t]*(?:const|let|var)\s+(?:[\w$]+|\{(?:[^{}=;]|\{(?:[^{}=;]|\{[^{}]*\})*\})*\}|\[[^\[\]=;]*\])\s*=\s*"""
    r"""require\(\s*(["'])[^"'\n]+\1\s*\)(?:\.[A-Za-z_$][\w$]*)?"""
    r"""(?:\s*;[ \t]*$|[ \t]*$(?!\s*[,.(\[`+\-*/%<>=&|?:]))""",
    re.MULTILINE,
)
"""A CommonJS `const x = require("m")` on its own line(s), with an optional `.member`; not one that goes on."""


_DESIGN_NOTES = """
# JS_REQUIRE_PATTERN — CommonJS Imports

## Purpose
What `remove_js_requires` cuts out: `const fs = require("fs")`,
`const { a, b: { c } } = require("m")`, `const [x] = require("m")`,
`var get = require("m").get`.

## A Statement That Goes On
Without a `;`, a statement ends at the end of its line only if the next line
cannot continue it. Comma-first style (`var a = require("a")` / `, b = require("b")`),
a chained `.call()` or an operator at the start of the next line mean the
declaration is not finished, and removing the first line would leave a broken
one. Such a statement is not taken.

## Limits
One declarator per statement (`const a = require("a"), b = require("b")` is not
taken), destructuring nested two levels deep and without default values (outside the innermost braces), and
the argument must be a plain string: `require(name)` is code, not a dependency.
"""
