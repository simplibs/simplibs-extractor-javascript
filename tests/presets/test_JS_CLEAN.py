import pytest
from simplibs.actions import Action
from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.extractor_javascript.logic._helpers import scan_js
from simplibs.extractor_javascript.presets import JS_CLEAN

SOURCE = (
    "// header\n"
    "import a from 'a';\n"
    "/**\n"
    " * Doc.\n"
    " */\n"
    "export function f(x) {\n"
    "  // inner\n"
    "  return x / 2 // half\n"
    "}\n"
    "\n"
    "\n"
    "\n"
    "const y = 1 /* c */\n"
)


def _body(text: str) -> str:
    """The text without the line breaks around it: the preset may or may not keep the final one."""
    return text.strip("\n")


def test_is_an_action() -> None:
    assert isinstance(JS_CLEAN, Action)


def test_the_error_of_the_first_step_comes_through(subtests) -> None:
    assert_action(
        subtests,
        JS_CLEAN,
        invalid_values=[5, None, b"x = 1"],
        expected_exception_type=ValidationError,
        deep_check=False,
        verbose=False,
    )


def test_the_comments_go_and_the_imports_and_exports_stay() -> None:
    result = JS_CLEAN(SOURCE)
    assert scan_js(result).comments == ()
    assert "import a from 'a';" in result
    assert "export function f(x) {" in result
    assert _body(result) == (
        "import a from 'a';\n"
        "export function f(x) {\n"
        "  return x / 2\n"
        "}\n"
        "\n"
        "const y = 1"
    )


def test_a_run_of_blank_lines_becomes_one_blank_line_not_none() -> None:
    result = JS_CLEAN("a = 1\n\n\n\n// c\n\n\nb = 2\n")
    assert "\n\n\n" not in result
    assert "a = 1\n\nb = 2" in result


def test_the_code_stays_in_paragraphs() -> None:
    result = JS_CLEAN("function a() {\n  return 1\n}\n\n\nfunction b() {\n  return 2\n}\n")
    assert "}\n\nfunction b()" in result


def test_a_comment_marker_in_a_literal_is_kept() -> None:
    result = JS_CLEAN("x = 'http://a' // c\ny = `// not ${ 1 }`\n")
    assert "'http://a'" in result
    assert "`// not ${ 1 }`" in result
    assert "// c" not in result


def test_a_text_that_needs_nothing_stays_as_it_is() -> None:
    text = "function f(a) {\n  return a\n}\n"
    assert _body(JS_CLEAN(text)) == _body(text)


def test_an_empty_text_stays_empty() -> None:
    assert JS_CLEAN("").strip() == ""


@pytest.mark.parametrize("text", [SOURCE, "x = 1 // c\n\n\n\ny = 2\n", "a/**/b\n"])
def test_a_second_run_changes_nothing(text) -> None:
    once = JS_CLEAN(text)
    assert JS_CLEAN(once) == once


def test_a_text_that_is_not_valid_javascript_is_not_a_card() -> None:
    assert isinstance(JS_CLEAN("x = (\n// c"), str)
