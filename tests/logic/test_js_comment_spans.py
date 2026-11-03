import pytest
from simplibs.exception import ValidationError
from simplibs.extractor_javascript.logic import js_comment_spans
from simplibs.extractor_javascript.logic._helpers import scan_js


def _found(text: str) -> list[str]:
    """The text of every span the function finds (the blanks in front of the comment included)."""
    return [text[start:end] for start, end in js_comment_spans(text)]


def test_a_text_without_comments_has_no_spans() -> None:
    assert js_comment_spans("const x = 1\nfunction f() {}\n") == []
    assert js_comment_spans("") == []


def test_returns_a_list_of_pairs_of_ints() -> None:
    spans = js_comment_spans("x = 1 // a\n/* b */\n")
    assert isinstance(spans, list)
    for span in spans:
        assert isinstance(span, tuple) and len(span) == 2
        assert all(isinstance(offset, int) for offset in span)


def test_a_line_comment_after_code_takes_the_blanks_in_front_of_it() -> None:
    assert _found("x = 1 // note\n") == [" // note"]


def test_a_line_comment_on_its_own_line_takes_its_indentation() -> None:
    assert _found("function f() {\n    // note\n    return 1\n}\n") == ["    // note"]


def test_a_block_comment() -> None:
    assert _found("x = 1 /* note */\n") == [" /* note */"]


def test_a_jsdoc_comment_over_several_lines() -> None:
    text = "/**\n * Adds.\n * @param {number} a\n */\nfunction add(a) {}\n"
    assert _found(text) == ["/**\n * Adds.\n * @param {number} a\n */"]


def test_the_comments_come_in_the_order_of_the_text() -> None:
    assert _found("// a\nx = 1 // b\n/* c */\ny\n") == ["// a", " // b", "/* c */"]


def test_every_comment_is_reported_also_those_that_need_a_space_when_cut() -> None:
    text = "a/**/b // c\n"
    assert _found(text) == ["/**/", " // c"]
    assert js_comment_spans(text) == list(scan_js(text).comments)


@pytest.mark.parametrize(
    "text",
    ["x = 'http://example.com'\n", 'x = "/* no */"\n', "x = `a // b`\n", "x = /[/*]/g\n", "x = <a>http://x.com</a>\n"],
    ids=["single", "double", "template", "regex-class", "jsx-text"],
)
def test_a_comment_marker_inside_a_literal_is_not_a_comment(text) -> None:
    assert js_comment_spans(text) == []


@pytest.mark.parametrize("text", ["'", '"', "`", "/*", "//", "/", "${", "`${", "/[", "'\\", "x = (\n// c", "</"])
def test_a_text_that_is_not_valid_javascript_never_raises(text) -> None:
    assert isinstance(js_comment_spans(text), list)


def test_works_for_typescript_and_jsx_alike() -> None:
    text = "const a: Array<number> = [] // list\nconst b = <div>{/* note */}</div>\n"
    assert _found(text) == [" // list", "/* note */"]


# ---------------------------------------------------------------- the arguments

@pytest.mark.parametrize("value", [None, 5, b"x = 1", ["x = 1"]])
def test_the_text_must_be_a_str(value) -> None:
    with pytest.raises(ValidationError):
        js_comment_spans(value)
