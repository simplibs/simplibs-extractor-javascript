import pytest
from simplibs.extractor_javascript.logic._helpers import skip_string


@pytest.mark.parametrize(
    "text, expected",
    [
        ('"abc"', 5),
        ("'abc'", 5),
        ('""', 2),
        ("''", 2),
        ('"abc" + 1', 5),
    ],
    ids=["double", "single", "empty-double", "empty-single", "followed-by-code"],
)
def test_the_end_is_just_after_the_closing_quote(text, expected) -> None:
    assert skip_string(text, 0) == expected


def test_the_other_kind_of_quote_inside_is_text() -> None:
    assert skip_string('"it\'s"', 0) == 6
    assert skip_string("'say \"hi\"'", 0) == 10


def test_an_escaped_quote_does_not_close_the_string() -> None:
    assert skip_string(r"'it\'s'", 0) == 7
    assert skip_string(r'"a\"b"', 0) == 6


def test_an_escaped_backslash_leaves_the_next_quote_free_to_close() -> None:
    assert skip_string(r"'a\\'", 0) == 5


def test_comment_markers_inside_a_string_are_text() -> None:
    assert skip_string('"http://example.com/*x*/"', 0) == 25


def test_a_line_continuation_keeps_the_string_going() -> None:
    assert skip_string("'a\\\nb'", 0) == 6


def test_it_starts_at_the_given_offset() -> None:
    assert skip_string("x = 'a' + 1", 4) == 7
    assert skip_string('f("a", "b")', 7) == 10


@pytest.mark.parametrize(
    "text, expected",
    [
        ('"abc\nnext', 4),
        ("'abc\nnext", 4),
        ("'\n", 1),
    ],
    ids=["double", "single", "nothing-before-the-break"],
)
def test_a_string_that_is_not_closed_ends_at_its_line(text, expected) -> None:
    """An apostrophe in JSX text (`<p>Don't</p>`) is no string; the damage stays on its line."""
    assert skip_string(text, 0) == expected


def test_a_string_that_is_not_closed_at_the_end_of_the_text() -> None:
    assert skip_string('"abc', 0) == 4


def test_a_backslash_at_the_very_end_does_not_run_past_the_text() -> None:
    assert skip_string("'a\\", 0) == 3


def test_wide_characters_inside() -> None:
    assert skip_string("'č€😀'", 0) == 5
