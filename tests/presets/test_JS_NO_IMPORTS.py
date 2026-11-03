import pytest
from simplibs.actions import Action
from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.extractor_javascript.logic._helpers import scan_js
from simplibs.extractor_javascript.presets import JS_NO_IMPORTS

SOURCE = (
    "// header\n"
    "import a from 'a' // the a\n"
    'const fs = require("fs")\n'
    "\n"
    "export const VERSION = 1\n"
    "\n"
    "export function run() {\n"
    "  return a // tail\n"
    "}\n"
    "\n"
    "export default run\n"
    "export { VERSION as V }\n"
)


def _body(text: str) -> str:
    """The text without the line breaks around it: the preset may or may not keep the final one."""
    return text.strip("\n")


def test_is_an_action() -> None:
    assert isinstance(JS_NO_IMPORTS, Action)


def test_the_error_of_the_first_step_comes_through(subtests) -> None:
    assert_action(
        subtests,
        JS_NO_IMPORTS,
        invalid_values=[5, None, b"x = 1"],
        expected_exception_type=ValidationError,
        deep_check=False,
        verbose=False,
    )


def test_only_the_logic_is_left() -> None:
    assert _body(JS_NO_IMPORTS(SOURCE)) == "const VERSION = 1\nfunction run() {\n  return a\n}"


def test_an_import_followed_by_a_comment_goes_because_the_comments_go_first() -> None:
    assert _body(JS_NO_IMPORTS('import a from "a" // the a\nrun(a)\n')) == "run(a)"


def test_nothing_of_the_wiring_is_left() -> None:
    result = JS_NO_IMPORTS(SOURCE)
    assert "import" not in result
    assert "require" not in result
    assert "export" not in result
    assert scan_js(result).comments == ()


def test_there_are_no_blank_lines_at_all() -> None:
    result = JS_NO_IMPORTS("import a from 'a'\n\n\nx = 1\n\n\n\ny = 2\n")
    assert "\n\n" not in result.strip("\n")
    assert _body(result) == "x = 1\ny = 2"


def test_an_anonymous_default_export_stays() -> None:
    assert _body(JS_NO_IMPORTS("import a from 'a'\nexport default () => a\n")) == "export default () => a"


def test_a_dynamic_import_stays() -> None:
    assert _body(JS_NO_IMPORTS('import a from "a"\nconst lazy = () => import("./lazy")\n')) == 'const lazy = () => import("./lazy")'


def test_a_class_keeps_its_methods() -> None:
    text = "import a from 'a'\n\nexport class A {\n  // note\n  m() {\n    return 1\n  }\n}\n"
    assert _body(JS_NO_IMPORTS(text)) == "class A {\n  m() {\n    return 1\n  }\n}"


def test_blank_lines_inside_a_template_literal_go_too() -> None:
    """Known, as with the Python preset: `COMPACT` does not know about strings."""
    assert _body(JS_NO_IMPORTS("const s = `a\n\nb`\n")) == "const s = `a\nb`"


@pytest.mark.parametrize("text", [SOURCE, "import a from 'a'\n\n\nx = 1 // c\n", "export default run\n"])
def test_a_second_run_changes_nothing(text) -> None:
    once = JS_NO_IMPORTS(text)
    assert JS_NO_IMPORTS(once) == once


def test_an_empty_text_stays_empty() -> None:
    assert JS_NO_IMPORTS("").strip() == ""
