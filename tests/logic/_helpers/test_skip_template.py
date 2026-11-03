import pytest
from simplibs.extractor_javascript.logic._helpers import skip_template


@pytest.mark.parametrize(
    "text",
    [
        "`abc`",
        "``",
        "`a // b`",
        "`a /* b */`",
        "`line one\nline two`",
        "`a\\`b`",
        "`cost: $5`",
        "`$a $ b`",
        "`${a}`",
        "`a ${b} c`",
        "`${ {a: 1}.a }`",
        "`${ {a: 1}.a + `x` }`",
        '`a ${ "}" } c`',
        "`a ${ '}' } c`",
        "`a ${ `b ${c}` } d`",
        "`${`${`${x}`}`}`",
        "`${ items.map(i => { return `<li>${i}</li>`; }).join('') }`",
        "`${ a / 2 }`",
        "`${ a / 2 + '}' }`",
        "`${ a /* } */ + b }`",
        "`${ a // }\n + b }`",
        "`${ s.replace(/'|\"/g, \"\") }`",
        "`${ /[}]/.test(s) }`",
        "`${ x }${ y }`",
    ],
    ids=[
        "plain", "empty", "line-comment-marker", "block-comment-marker", "several-lines", "escaped-backtick", "dollar-digit",
        "dollar-space", "expression", "expression-in-text", "object-in-expression", "object-then-nested-template", "string-with-brace", "single-string-with-brace",
        "nested-template", "triple-nested", "arrow-with-template", "division", "division-then-string", "block-comment-with-brace",
        "line-comment-with-brace", "regex-with-quotes", "regex-with-brace-in-class", "two-expressions",
    ],
)
def test_a_template_is_skipped_whole(text) -> None:
    assert skip_template(text, 0) == len(text)


def test_the_end_is_just_after_the_closing_backtick() -> None:
    assert skip_template("`abc` + 1", 0) == 5
    assert skip_template("`a${b}` + 1", 0) == 7


def test_it_starts_at_the_given_offset() -> None:
    assert skip_template("x = `a${b}`;", 4) == 11
    assert skip_template("f(`a`, `b`)", 7) == 10


def test_a_template_that_is_not_closed_runs_to_the_end_of_the_text() -> None:
    """Unlike a quoted string, a template may span lines, so there is no line to stop at."""
    assert skip_template("`abc", 0) == 4
    assert skip_template("`abc\nmore code\n", 0) == 15


def test_an_expression_that_is_not_closed_runs_to_the_end_of_the_text() -> None:
    assert skip_template("`${ a", 0) == 5
    assert skip_template("`${ a }", 0) == 7


def test_a_backslash_at_the_very_end_does_not_run_past_the_text() -> None:
    assert skip_template("`a\\", 0) == 3


def test_the_code_after_a_template_is_not_taken_into_it() -> None:
    text = "`a ${ '}' } c` + `b`"
    assert skip_template(text, 0) == 14


def test_wide_characters_inside() -> None:
    assert skip_template("`č€😀 ${ 'ž' }`", 0) == 14
