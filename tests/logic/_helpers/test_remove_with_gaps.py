import pytest
from simplibs.extractor_javascript.logic._helpers import remove_with_gaps


def test_without_gaps_it_only_cuts() -> None:
    assert remove_with_gaps("a /* c */ b", [(1, 9)], []) == "a b"


def test_without_spans_the_text_stays_as_it_is() -> None:
    assert remove_with_gaps("a b", [], []) == "a b"


def test_a_gap_leaves_a_single_space() -> None:
    assert remove_with_gaps("a/**/b", [(1, 5)], [(1, 5)]) == "a b"


def test_without_the_gap_the_tokens_would_grow_together() -> None:
    assert remove_with_gaps("a/**/b", [(1, 5)], []) == "ab"


def test_two_gaps() -> None:
    assert remove_with_gaps("a/**/b/**/c", [(1, 5), (6, 10)], [(1, 5), (6, 10)]) == "a b c"


def test_a_gap_next_to_a_cut_that_needs_none() -> None:
    assert remove_with_gaps("a/**/b /* x */ c", [(1, 5), (6, 14)], [(1, 5)]) == "a b c"


def test_only_the_spans_that_are_gaps_leave_a_space() -> None:
    assert remove_with_gaps("a/**/b/**/c", [(1, 5), (6, 10)], [(6, 10)]) == "ab c"


def test_a_gap_at_the_very_start_puts_the_space_in_front() -> None:
    assert remove_with_gaps("/**/a", [(0, 4)], [(0, 4)]) == " a"


def test_the_same_gap_twice_leaves_one_space() -> None:
    assert remove_with_gaps("a/**/b", [(1, 5)], [(1, 5), (1, 5)]) == "a b"


def test_the_gaps_may_be_any_collection() -> None:
    for gaps in ([(1, 5)], ((1, 5),), {(1, 5)}, frozenset({(1, 5)})):
        assert remove_with_gaps("a/**/b", [(1, 5)], gaps) == "a b"


def test_the_spans_may_be_any_sequence() -> None:
    assert remove_with_gaps("a/**/b", ((1, 5),), ((1, 5),)) == "a b"


def test_wide_characters_in_front_of_the_gap() -> None:
    assert remove_with_gaps("č€😀/**/b", [(3, 7)], [(3, 7)]) == "č€😀 b"


def test_a_line_that_held_only_a_removed_span_disappears_whole() -> None:
    assert remove_with_gaps("x\n/* c */\ny", [(2, 9)], []) == "x\ny"


def test_the_gaps_and_a_whole_line_together() -> None:
    text = "a/**/b\n// note\nc"
    assert remove_with_gaps(text, [(1, 5), (7, 14)], [(1, 5)]) == "a b\nc"
