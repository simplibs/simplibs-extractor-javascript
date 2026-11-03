import time
import pytest
from simplibs.extractor_javascript.logic._helpers import JsScan, scan_js


def _comments(text: str) -> list[str]:
    return [text[start:end] for start, end in scan_js(text).comments]


def _glued(text: str) -> list[str]:
    return [text[start:end] for start, end in scan_js(text).glued]


def _literals(text: str) -> list[str]:
    return [text[start:end] for start, end in scan_js(text).literals]


def test_returns_a_scan() -> None:
    assert isinstance(scan_js("x = 1\n"), JsScan)


def test_the_three_lists_are_tuples() -> None:
    scan = scan_js("x = 'a' // c\n")
    assert isinstance(scan.comments, tuple) and isinstance(scan.glued, tuple) and isinstance(scan.literals, tuple)


@pytest.mark.parametrize("text", ["", " ", "\n", "x = 1\n", "function f() { return 1 }\n"])
def test_a_text_without_comments_and_literals_finds_nothing(text) -> None:
    assert scan_js(text) == JsScan((), (), ())


# ---------------------------------------------------------------- line comments

def test_a_line_comment_after_code_takes_the_blanks_in_front_of_it() -> None:
    assert _comments("x = 1 // note\n") == [" // note"]


def test_a_line_comment_on_its_own_line_takes_its_indentation() -> None:
    assert _comments("function f() {\n    // note\n    return 1\n}\n") == ["    // note"]


def test_a_tab_in_front_is_a_blank_too() -> None:
    assert _comments("x = 1\t// note\n") == ["\t// note"]


def test_a_line_comment_at_the_end_of_a_text_without_a_final_newline() -> None:
    assert _comments("x = 1 // note") == [" // note"]


def test_a_line_comment_does_not_take_the_line_break() -> None:
    text = "x = 1 // note\ny = 2\n"
    ((start, end),) = scan_js(text).comments
    assert text[end] == "\n"


def test_several_comments_come_in_the_order_of_the_text() -> None:
    assert _comments("// a\nx = 1 // b\n/* c */\ny\n") == ["// a", " // b", "/* c */"]


def test_a_line_comment_hides_a_block_comment_marker() -> None:
    assert _comments("x // a /* b\ny */ z\n") == [" // a /* b"]


# ---------------------------------------------------------------- block comments

def test_a_block_comment_followed_by_a_blank_takes_the_blanks_in_front_of_it() -> None:
    text = "a /* c */ b"
    assert _comments(text) == [" /* c */"]
    assert _glued(text) == []


def test_a_block_comment_at_the_end_of_a_line() -> None:
    assert _comments("x = 1 /* c */\ny\n") == [" /* c */"]


def test_a_block_comment_over_several_lines() -> None:
    assert _comments("a\n/* one\ntwo */\nb") == ["/* one\ntwo */"]


def test_a_block_comment_between_two_tokens_with_no_blank_is_glued() -> None:
    text = "a/**/b"
    assert _comments(text) == ["/**/"]
    assert _glued(text) == ["/**/"]


def test_a_glued_comment_is_also_one_of_the_comments() -> None:
    scan = scan_js("a/**/b + c/**/d")
    assert set(scan.glued) <= set(scan.comments)
    assert len(scan.glued) == 2


@pytest.mark.parametrize(
    "text",
    ["a/**/+b", "1/**/2", "$/**/_", "x/* c */y", "a/**/b"],
    ids=["word-and-operator", "numbers", "dollar-and-underscore", "longer-comment", "words"],
)
def test_any_two_tokens_that_would_grow_together_make_a_glued_comment(text) -> None:
    assert len(scan_js(text).glued) == 1


@pytest.mark.parametrize(
    "text",
    ["(/* c */a)", "a(/**/)", "[/**/1]", "{/**/}", "f(a,/**/b)", "a;/**/b", "/* c */x", "x/* c */"],
    ids=["after-bracket", "between-brackets", "square", "curly", "after-comma", "after-semicolon", "at-start", "at-end"],
)
def test_a_separator_on_either_side_means_no_space_is_needed(text) -> None:
    scan = scan_js(text)
    assert len(scan.comments) == 1
    assert scan.glued == ()


def test_a_block_comment_that_is_never_closed_runs_to_the_end_of_the_text() -> None:
    text = "x /* open\nmore"
    assert _comments(text) == [" /* open\nmore"]


# ---------------------------------------------------------------- strings, templates, regular expressions

def test_the_literals_are_found_with_their_quotes() -> None:
    assert _literals("a = 'x' + \"y\"") == ["'x'", '"y"']


def test_a_template_literal_is_a_literal() -> None:
    assert _literals("a = `x ${ y }`") == ["`x ${ y }`"]


def test_a_line_comment_marker_in_a_string_is_text() -> None:
    text = 'x = "http://example.com" // real'
    assert _comments(text) == [" // real"]
    assert _literals(text) == ['"http://example.com"']


def test_a_block_comment_marker_in_a_string_is_text() -> None:
    text = "x = '/* not */' + 1"
    assert _comments(text) == []
    assert _literals(text) == ["'/* not */'"]


def test_comment_markers_in_a_template_are_text() -> None:
    text = "x = `a // b ${ c /* d */ } e` // real"
    assert _comments(text) == [" // real"]
    assert _literals(text) == ["`a // b ${ c /* d */ } e`"]


def test_a_comment_marker_in_a_regex_class_is_text() -> None:
    assert _comments("const r = /[/*]/g // note\n") == [" // note"]


def test_a_quote_in_a_regex_does_not_open_a_string() -> None:
    text = "f(/'/); // c"
    assert _comments(text) == [" // c"]
    assert _literals(text) == []


def test_a_regex_after_return_and_after_an_arrow() -> None:
    assert _comments("return /\"/.test(y) // c") == [" // c"]
    assert _comments("f = () => /a'/.test(x) // c") == [" // c"]


def test_a_regex_after_a_colon_and_after_a_comma() -> None:
    assert _comments("x = { a: /b'/ } // c") == [" // c"]
    assert _comments("f(1, /'/) // c") == [" // c"]


def test_a_division_is_not_a_regex() -> None:
    text = "a = b / c // d"
    assert _comments(text) == [" // d"]
    assert _comments("a = (b) / c // d") == [" // d"]
    assert _comments("a = arr[0] / 2 // d") == [" // d"]
    assert _comments("Array<T> / 2 // d") == [" // d"]


def test_a_regex_after_a_finished_regex_is_a_division() -> None:
    assert _comments("a = /x/ / 2 // d") == [" // d"]


def test_a_closing_jsx_tag_is_not_a_regex() -> None:
    assert _comments("x = <div>a</div> // c") == [" // c"]


def test_a_comparison_with_a_regex_after_a_less_than_sign() -> None:
    assert _comments("ok = n </a'b/.test(s) // c") == [" // c"]


def test_a_url_in_jsx_text_is_no_comment() -> None:
    assert _comments("x = <a>http://example.com</a>\n") == []


def test_a_comment_right_after_a_colon_is_kept_as_known_price() -> None:
    """Documented: `case 1://note` keeps its comment, because `://` is the mark of a URL."""
    assert _comments("case 1://note\n") == []


def test_a_comment_after_a_colon_and_a_blank_is_a_comment() -> None:
    assert _comments("case 1: // note\n") == [" // note"]


# ---------------------------------------------------------------- errors stay on one line

def test_a_string_that_is_not_closed_ends_at_its_line_and_the_next_line_is_code_again() -> None:
    text = "a = 'it\nb = 1 // c\n"
    assert _literals(text) == ["'it"]
    assert _comments(text) == [" // c"]


def test_an_apostrophe_in_jsx_text_spoils_only_its_line() -> None:
    text = "x = <p>Don't</p>\n// c\n"
    assert _comments(text) == ["// c"]


def test_a_slash_taken_for_a_regex_that_is_not_closed_on_its_line_is_code_again() -> None:
    text = "x = (1) / 2 + a(/b\n// c\n"
    assert _comments(text) == ["// c"]


# ---------------------------------------------------------------- the guarantees of the design notes

SAMPLES = [
    "x = 1 // a\n/* b */ y = 'c // d'\n",
    "const s = `a // b ${ c /* d */ } e` // f\n",
    "a/**/b + /[/*]/.test(c) // d\n",
    "<div>http://x.com</div> // e\n",
    "f(/'/, \"/*\", `//`) /* g */\n",
    "x = 'it\nnext // c\n",
    "",
]


@pytest.mark.parametrize("text", SAMPLES)
def test_no_comment_overlaps_a_literal(text) -> None:
    scan = scan_js(text)
    for c_start, c_end in scan.comments:
        for l_start, l_end in scan.literals:
            assert c_end <= l_start or l_end <= c_start, (text, (c_start, c_end), (l_start, l_end))


@pytest.mark.parametrize("text", SAMPLES)
def test_the_spans_are_in_the_order_of_the_text_and_inside_it(text) -> None:
    scan = scan_js(text)
    for spans in (scan.comments, scan.glued, scan.literals):
        assert list(spans) == sorted(spans)
        for start, end in spans:
            assert 0 <= start < end <= len(text)


@pytest.mark.parametrize("text", SAMPLES)
def test_it_never_fails_whatever_the_text(text) -> None:
    assert isinstance(scan_js(text), JsScan)


@pytest.mark.parametrize("text", ["'", '"', "`", "/*", "//", "/", "${", "`${", "/[", "'\\", "\\", "a/", "</", "`${`"])
def test_a_broken_text_is_scanned_without_an_error(text) -> None:
    assert isinstance(scan_js(text), JsScan)


def test_wide_characters_do_not_move_the_spans() -> None:
    text = "x = 'č€😀' // čau\n"
    assert _literals(text) == ["'č€😀'"]
    assert _comments(text) == [" // čau"]


def test_a_long_text_is_scanned_in_reasonable_time() -> None:
    text = "const a = 'x' /* b */ + c / d // e\n" * 5000
    started = time.perf_counter()
    scan = scan_js(text)
    assert time.perf_counter() - started < 5
    assert len(scan.comments) == 10000
