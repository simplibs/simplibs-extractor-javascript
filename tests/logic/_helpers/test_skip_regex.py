import pytest
from simplibs.extractor_javascript.logic._helpers import skip_regex


@pytest.mark.parametrize(
    "text, expected",
    [
        ("/abc/", 5),
        ("/abc/ + 1", 5),
        ("/a/", 3),
        ("//", 2),
    ],
    ids=["plain", "followed-by-code", "short", "empty-body"],
)
def test_the_end_is_just_after_the_closing_slash(text, expected) -> None:
    assert skip_regex(text, 0) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("/abc/g;", 6),
        ("/abc/gi;", 7),
        ("/abc/gimsuy;", 11),
        ("/a/é;", 4),
        ("/a/g1;", 5),
    ],
    ids=["one-flag", "two-flags", "many-flags", "letter-of-any-script", "digit-after-flag"],
)
def test_the_flags_belong_to_the_literal(text, expected) -> None:
    assert skip_regex(text, 0) == expected


def test_a_slash_in_a_class_does_not_close_the_literal() -> None:
    assert skip_regex("/[/]/g", 0) == 6
    assert skip_regex("/[a/b]x/", 0) == 8


def test_an_escaped_bracket_does_not_end_the_class() -> None:
    assert skip_regex(r"/[\]/]/", 0) == 7


def test_an_escaped_slash_does_not_close_the_literal() -> None:
    assert skip_regex(r"/a\/b/", 0) == 6
    assert skip_regex(r"/\//g", 0) == 5


@pytest.mark.parametrize(
    "text, expected",
    [
        ("/\"/", 3),
        ("/'/", 3),
        ("/'|\"/g", 6),
        ("/[/*]/", 6),
        ("/a*/", 4),
        ("/`/", 3),
    ],
    ids=["double-quote", "single-quote", "both-quotes", "comment-marker-in-class", "star", "backtick"],
)
def test_characters_that_would_open_a_string_or_a_comment_are_skipped(text, expected) -> None:
    assert skip_regex(text, 0) == expected


def test_it_starts_at_the_given_offset() -> None:
    assert skip_regex("a = /x/g;", 4) == 8
    assert skip_regex("f(/a/, /b/)", 7) == 10


def test_a_line_that_ends_first_means_it_was_no_regex_after_all() -> None:
    """Only the slash itself is consumed, and scanning goes on with the rest of the line as code."""
    assert skip_regex("/abc\nmore/", 0) == 1
    assert skip_regex("x = a /b\nc/", 6) == 7


def test_a_literal_that_is_never_closed_runs_to_the_end_of_the_text() -> None:
    assert skip_regex("/abc", 0) == 4


def test_a_backslash_at_the_very_end_does_not_run_past_the_text() -> None:
    assert skip_regex("/a\\", 0) == 3


def test_the_result_never_goes_beyond_the_text_by_more_than_the_escape_jump() -> None:
    for text in ["/", "/\\", "/[", "/[\\", "/a[\\"]:
        assert skip_regex(text, 0) <= len(text) + 1
