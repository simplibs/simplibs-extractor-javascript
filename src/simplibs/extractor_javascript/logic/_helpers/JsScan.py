from dataclasses import dataclass
from simplibs.text.annotations import Span


@dataclass(frozen=True, slots=True)
class JsScan:
    """What the scanner found in a JavaScript or TypeScript source.

    Attributes:
        comments: The spans of every comment, with the blanks in front of it where they can go.
        glued: The comments (a subset of `comments`) that sit between two tokens with no blank
            around them; a space has to be left in their place.
        literals: The spans of every string and template literal.
    """

    comments: tuple[Span, ...]
    glued: tuple[Span, ...]
    literals: tuple[Span, ...]


_DESIGN_NOTES = """
# JsScan — The Result of One Pass

## Purpose
The scanner reads a source once and answers three questions at the same time:
where are the comments, which of them need a space in their place, and where
are the literals (the places the import and export steps must not look into).

## Why a Frozen Record
The three lists belong together and are not changed after the scan.
"""
