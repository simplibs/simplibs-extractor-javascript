import re
from bisect import bisect_right
# Inners
from .JsScan import JsScan


def find_matches_outside(text: str, pattern: re.Pattern[str], scan: JsScan) -> list[re.Match[str]]:
    """Find the matches of a line pattern that do not start inside a literal or a comment.

    Args:
        text: The source.
        pattern: A pattern that matches whole statements at the start of a line.
        scan: The result of `scan_js` for `text`.

    Returns:
        The matches that start in code.
    """

    # 1. The places the pattern must not start in: strings, templates, comments
    protected = sorted(scan.literals + scan.comments)
    starts = [start for start, _ in protected]

    # 2. A match that begins inside one is text of that string or comment, not a statement
    found: list[re.Match[str]] = []
    for match in pattern.finditer(text):
        index = bisect_right(starts, match.start()) - 1
        if index >= 0 and match.start() < protected[index][1]:
            continue
        found.append(match)

    return found


_DESIGN_NOTES = """
# find_matches_outside — A Statement Must Be in the Code

## Purpose
The import, require and export steps find statements by line patterns. A line
that LOOKS like `import a from "b"` inside a template literal (a code sample
in a string) or inside a block comment is not a statement. The scan knows
where those are.

## Why Comments Count
The steps do not depend on running after `strip_js_comments`: an import inside a
`/* ... */` block is found and left alone either way.
"""
