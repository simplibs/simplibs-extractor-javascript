from typing import Final
from simplibs.path.rules import NameIs
from simplibs.rules import Rule, StartsWith


UNDERSCORE_NAME: Final[Rule] = NameIs(StartsWith("_"))
"""The file name starts with an underscore (`_app.tsx`, `_helpers.js`)."""


_DESIGN_NOTES = """
# UNDERSCORE_NAME — Private by Convention

## Purpose
In JavaScript projects a leading underscore marks a private helper, and in
Next.js `_app.tsx` and `_document.tsx` are central. `build_js_base()` decides
by its `include_underscore` option whether they are taken.
"""
