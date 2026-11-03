from simplibs.validate import validate_call
# Inners
from ._helpers import remove_with_gaps, scan_js


@validate_call
def strip_js_comments(text: str) -> str:
    """Remove all comments from a JavaScript or TypeScript source, JSDoc included.

    Args:
        text: The source.

    Returns:
        The text without comments. A line that held only a comment disappears.
        `{/* note */}` in JSX leaves `{}`.
    """

    # 1. One pass finds the comments and which of them sit between two tokens
    scan = scan_js(text)

    # 2. Cut them; a comment between two tokens leaves a space
    return remove_with_gaps(text, scan.comments, scan.glued)


_DESIGN_NOTES = """
# strip_js_comments — The Comments Out, The Strings Untouched

## Purpose
A step of the profiles `javascript/code-clean`, `javascript/code-no-imports` and
`javascript/src-clean`. Works for JavaScript, TypeScript, JSX and TSX alike: the
scanner needs no knowledge of types or tags to find a comment.

## Guarantee
For a source that parses, the syntax tree of the result equals the tree of the
original, apart from positions.

## Known Limits
* A block comment that holds a line break between two tokens on one line
  (`return /* \\n */ x`) changes what the JavaScript line-ending rules see.
* `{/* note */}` leaves `{}`: removing the brackets needs a JSX parser.
* A slash taken for a division where it starts a regex (after `)` or `}`) can
  hide one comment on that line.
"""
