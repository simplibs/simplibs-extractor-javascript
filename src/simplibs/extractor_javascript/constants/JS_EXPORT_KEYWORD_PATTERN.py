import re
from typing import Final


JS_EXPORT_KEYWORD_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^([ \t]*)export\s+(?:default\s+(?=(?:async\s+)?function\s*\*?\s*[A-Za-z_$]"
    r"|class\s+(?!extends\b)[A-Za-z_$])"
    r"|(?=(?:declare\s+)?(?:async\s+)?(?:function|class|const|let|var|interface|type|enum|abstract)\b))",
    re.MULTILINE,
)
"""The keywords `export` or `export default` in front of a NAMED declaration; group 1 is the indentation."""


_DESIGN_NOTES = """
# JS_EXPORT_KEYWORD_PATTERN — Only the Keyword Goes

## Purpose
`export function f() {}`, `export const a = 1`, `export default class App {}`,
`export interface Props {}`: the declaration is the code, `export` is only
visibility. The match covers the keyword (and `default`) up to the declaration;
group 1 is the indentation, which stays.

## An Anonymous Default Stays
`export default function () {}` and `export default class extends X {}` have
no name: without `export default` they would not be valid statements.
"""
