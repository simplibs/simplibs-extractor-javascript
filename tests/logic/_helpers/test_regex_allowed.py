import pytest
from simplibs.extractor_javascript.constants import JS_REGEX_KEYWORDS
from simplibs.extractor_javascript.logic._helpers import regex_allowed


# ---------------------------------------------------------------- after `>`

def test_after_an_arrow_a_slash_starts_a_regex() -> None:
    assert regex_allowed(">", "", before_last="=") is True


@pytest.mark.parametrize("before_last", ["", "T", ")", "-", " "])
def test_after_any_other_closing_angle_bracket_a_slash_divides(before_last) -> None:
    """`Array<T> / 2`: the `>` closes a type, or is a comparison."""
    assert regex_allowed(">", "", before_last=before_last) is False


def test_the_angle_bracket_wins_over_a_word() -> None:
    assert regex_allowed(">", "return", before_last="x") is False


# ---------------------------------------------------------------- after `<`

def test_after_a_less_than_sign_a_slash_is_a_regex_when_no_closing_tag_follows() -> None:
    """`n </image\\/x/.test(s)` compares with a regex literal."""
    assert regex_allowed("<", "", closing_tag=False) is True


def test_after_a_less_than_sign_a_slash_that_ends_a_tag_is_no_regex() -> None:
    """`</div>` closes a JSX element."""
    assert regex_allowed("<", "", closing_tag=True) is False


# ---------------------------------------------------------------- where an expression begins

def test_at_the_start_of_the_text_a_slash_starts_a_regex() -> None:
    assert regex_allowed("", "") is True


@pytest.mark.parametrize("last", list("(,=:[!&|?{;+-*%~^"))
def test_after_an_operator_or_an_opening_bracket_a_slash_starts_a_regex(last) -> None:
    assert regex_allowed(last, "") is True


# ---------------------------------------------------------------- after a word

@pytest.mark.parametrize("word", sorted(JS_REGEX_KEYWORDS))
def test_after_a_keyword_that_begins_an_expression_a_slash_starts_a_regex(word) -> None:
    assert regex_allowed(word[-1], word) is True


@pytest.mark.parametrize("word", ["x", "total", "this", "null", "true", "undefined", "42", "a1", "returns", "returned", "_return", "$"])
def test_after_any_other_word_or_number_a_slash_divides(word) -> None:
    assert regex_allowed(word[-1], word) is False


def test_a_keyword_only_counts_as_a_whole_word() -> None:
    """`returns / 2` divides a variable called `returns`."""
    assert regex_allowed("s", "returns") is False
    assert regex_allowed("n", "return") is True


# ---------------------------------------------------------------- after a value

@pytest.mark.parametrize("last", [")", "]", "}", '"', "`", "/"])
def test_after_a_closing_bracket_a_literal_or_a_slash_a_slash_divides(last) -> None:
    assert regex_allowed(last, "") is False


def test_after_a_regex_literal_a_slash_divides() -> None:
    """The scanner records a finished regex as the character `x`, a value."""
    assert regex_allowed("x", "") is False


def test_after_a_closing_parenthesis_it_is_a_division_even_where_it_is_wrong() -> None:
    """Known heuristic: `if (x) /re/.test(y)` is read as a division; the damage stays on one line."""
    assert regex_allowed(")", "") is False


def test_after_a_closing_brace_it_is_a_division_even_where_it_is_wrong() -> None:
    assert regex_allowed("}", "") is False


def test_returns_a_real_bool() -> None:
    for arguments in [("", ""), (")", ""), ("n", "return"), ("<", "")]:
        assert type(regex_allowed(*arguments)) is bool
