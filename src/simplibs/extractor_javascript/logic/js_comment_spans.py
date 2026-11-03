from simplibs.validate import validate_call
from simplibs.text.annotations import Span
# Inners
from ._helpers import scan_js


@validate_call
def js_comment_spans(text: str) -> list[Span]:
    """Find the comments of a JavaScript or TypeScript source.

    Args:
        text: The source.

    Returns:
        A span for each comment (`//` and `/* */`, JSDoc included), from the blanks in front of it
        to its end.
    """

    # 1. The comments the scanner found
    return list(scan_js(text).comments)


_DESIGN_NOTES = """
# js_comment_spans — Where the Comments Are

## Purpose
The spans of the comments, for anything that wants to look at them or cut them.
`strip_js_comments` also knows which of them need a space left behind; this
function reports every one of them.

## Never Raises
The scanner has no syntax it refuses: whatever the text is, it gets an answer.
"""
