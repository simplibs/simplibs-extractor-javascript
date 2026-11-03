import re
from typing import Final


JS_CLOSING_TAG: Final[re.Pattern[str]] = re.compile(r"/[\w$.:\-]*\s*>")
"""What follows the `<` of a JSX closing tag: `/div>`, `/Foo.Bar >`, `/>` of a fragment."""


_DESIGN_NOTES = """
# JS_CLOSING_TAG — `</div>` or `0 </re/`?

## Purpose
After a `<`, a slash is either the start of a JSX closing tag (`</div>`) or of a
regular expression (`n </image\\/x/.test(s)`, a comparison with a literal).
A closing tag is a slash, a tag name and `>`; anything else is a regex.

## Matched at the Slash
The pattern is tried at the position of the slash with `Pattern.match`.
"""
