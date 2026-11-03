from bisect import bisect_right
from collections.abc import Collection, Sequence
from simplibs.text import remove_spans
from simplibs.text.annotations import Span


def remove_with_gaps(text: str, spans: Sequence[Span], gaps: Collection[Span]) -> str:
    """Remove spans from a text, leaving one space where a span was marked as a gap.

    Args:
        text: The text.
        spans: The ranges to remove.
        gaps: The spans (a subset of `spans`) that leave a single space behind.

    Returns:
        The text without the spans.
    """

    # 1. A space goes in front of every gap; the cut then removes the span and leaves the space
    positions = sorted({start for start, _ in gaps})
    pieces: list[str] = []
    previous = 0
    for position in positions:
        pieces.append(text[previous:position])
        pieces.append(" ")
        previous = position
    pieces.append(text[previous:])
    padded = "".join(pieces)

    # 2. The spans move with the text: each space inserted at or before an offset pushes it by one
    shifted = [
        (start + bisect_right(positions, start), end + bisect_right(positions, end))
        for start, end in spans
    ]

    # 3. Cut; a line that held only a removed span disappears whole
    return remove_spans(padded, shifted)


_DESIGN_NOTES = """
# remove_with_gaps — Cutting Without Gluing

## Purpose
`remove_spans` only removes. A block comment between two tokens must leave a
space (`a/**/b` is `a b`, not `ab`). The space is put in first, the span is
cut after, so one primitive does both.

## Shifting
Every inserted space moves all later offsets by one; the spans are shifted by
the number of spaces at or before them.
"""
