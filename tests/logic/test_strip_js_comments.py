import pytest
from simplibs.exception import ValidationError
from simplibs.extractor_javascript.logic import strip_js_comments
from simplibs.extractor_javascript.logic._helpers import scan_js

SAMPLES = [
    "x = 1 // note\n",
    "// only\nx = 1\n",
    "function f() {\n    // c\n    return 1\n}\n",
    "/**\n * Doc.\n */\nfunction f() {}\n",
    "a = 1 // x\n/* y */ b = 2\n",
    "const s = `a // b ${ c /* d */ } e` // f\n",
    "x = 'http://a' // c\n",
    "a/**/b + (/* c */d)\n",
    "x = a / b // c\n",
    "const r = /[/*]/g // c\n",
    "x = <div>{/* note */}</div>\n",
    "",
]


@pytest.mark.parametrize(
    "text, expected",
    [
        ("x = 1 // note\n", "x = 1\n"),
        ("x = 1 // note", "x = 1"),
        ("// only\nx = 1\n", "x = 1\n"),
        ("x = 1\n// between\ny = 2\n", "x = 1\ny = 2\n"),
        ("function f() {\n    // c\n    return 1\n}\n", "function f() {\n    return 1\n}\n"),
        ("x = 1 /* c */\ny = 2\n", "x = 1\ny = 2\n"),
        ("/* a */\nx = 1\n", "x = 1\n"),
        ("/**\n * Doc.\n * @param a\n */\nfunction f(a) {}\n", "function f(a) {}\n"),
        ("a /* c */ b", "a b"),
        ("f(a, /* c */ b)", "f(a, b)"),
        ("x = a / b // c\n", "x = a / b\n"),
        ('x = "č€😀" // čau\n', 'x = "č€😀"\n'),
    ],
    ids=[
        "after-code", "no-final-newline", "own-line", "between", "indented", "block-after-code", "block-own-line", "jsdoc",
        "between-two-words", "in-arguments", "division", "wide-characters",
    ],
)
def test_the_comments_go_and_the_code_stays(text, expected) -> None:
    assert strip_js_comments(text) == expected


def test_a_text_that_holds_only_comments_becomes_empty() -> None:
    assert strip_js_comments("// a\n/* b */\n") == ""


def test_an_empty_text_stays_empty() -> None:
    assert strip_js_comments("") == ""


def test_a_text_without_comments_stays_as_it_is() -> None:
    text = "function f(a,b){\n  return  a+b\n}\n"
    assert strip_js_comments(text) == text


# ---------------------------------------------------------------- a comment between two tokens

@pytest.mark.parametrize(
    "text, expected",
    [
        ("a/**/b", "a b"),
        ("1/**/2", "1 2"),
        ("a/**/+b", "a +b"),
        ("return/**/x", "return x"),
        ("a/* c */b/* d */c", "a b c"),
    ],
    ids=["words", "numbers", "word-and-operator", "keyword", "two-comments"],
)
def test_a_comment_that_stood_between_two_tokens_leaves_a_space(text, expected) -> None:
    """Without it `a/**/b` would become the one name `ab`."""
    assert strip_js_comments(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("(/* c */a)", "(a)"),
        ("f(/**/)", "f()"),
        ("[/**/1]", "[1]"),
        ("f(a,/**/b)", "f(a,b)"),
        ("a;/**/b", "a;b"),
    ],
    ids=["after-bracket", "between-brackets", "square", "after-comma", "after-semicolon"],
)
def test_a_comment_next_to_a_separator_leaves_nothing(text, expected) -> None:
    assert strip_js_comments(text) == expected


def test_a_comment_in_jsx_leaves_its_braces_as_documented() -> None:
    """Removing the brackets too would need a JSX parser."""
    assert strip_js_comments("x = <div>{/* note */}</div>\n") == "x = <div>{}</div>\n"


# ---------------------------------------------------------------- what is never touched

@pytest.mark.parametrize(
    "text",
    [
        "x = 'http://example.com'\n",
        'x = "/* no */"\n',
        "x = `// a ${ b /* c */ } d`\n",
        "const r = /[/*]/g\n",
        "const r = /'/\n",
        "x = <a>http://x.com</a>\n",
        "x = a / b / c\n",
    ],
    ids=["single", "double", "template", "regex-class", "regex-quote", "jsx-text", "divisions"],
)
def test_a_comment_marker_inside_a_literal_is_never_touched(text) -> None:
    assert strip_js_comments(text) == text


def test_a_string_next_to_a_comment() -> None:
    assert strip_js_comments('x = "a // b" // real\n') == 'x = "a // b"\n'


def test_a_regex_next_to_a_comment() -> None:
    assert strip_js_comments("const r = /[/*]/g // note\n") == "const r = /[/*]/g\n"


def test_a_template_with_an_expression_next_to_a_comment() -> None:
    text = "const s = `a // b ${ c /* d */ } e` // f\n"
    assert strip_js_comments(text) == "const s = `a // b ${ c /* d */ } e`\n"


# ---------------------------------------------------------------- the guarantees of the design notes

@pytest.mark.parametrize("text", SAMPLES)
def test_no_comment_is_left(text) -> None:
    assert scan_js(strip_js_comments(text)).comments == ()


@pytest.mark.parametrize("text", SAMPLES)
def test_a_second_run_changes_nothing(text) -> None:
    once = strip_js_comments(text)
    assert strip_js_comments(once) == once


@pytest.mark.parametrize("text", SAMPLES)
def test_every_literal_survives_unchanged(text) -> None:
    before = [text[start:end] for start, end in scan_js(text).literals]
    result = strip_js_comments(text)
    after = [result[start:end] for start, end in scan_js(result).literals]
    assert after == before


@pytest.mark.parametrize("text", ["'", '"', "`", "/*", "//", "/", "${", "`${", "/[", "'\\", "x = (\n// c", "</"])
def test_a_text_that_is_not_valid_javascript_never_raises(text) -> None:
    assert isinstance(strip_js_comments(text), str)


def test_an_unterminated_block_comment_takes_the_rest_of_the_text() -> None:
    assert strip_js_comments("x = 1 /* open\nmore code\n") == "x = 1"


# ---------------------------------------------------------------- the arguments

@pytest.mark.parametrize("value", [None, 5, b"x = 1", ["x = 1"]])
def test_the_text_must_be_a_str(value) -> None:
    with pytest.raises(ValidationError):
        strip_js_comments(value)
