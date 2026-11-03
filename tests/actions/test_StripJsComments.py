import pytest
from simplibs.actions import Action
from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.extractor_javascript.actions import RemoveJsImports, StripJsComments
from simplibs.extractor_javascript.logic import remove_js_imports, strip_js_comments

SAMPLES = [
    "x = 1 // note\n",
    "// only\nx = 1\n",
    "function f() {\n    // c\n    return 1\n}\n",
    "a/**/b + (/* c */d)\n",
    "x = 'http://a' // c\n",
    "",
]


def test_the_action_contract(subtests) -> None:
    assert_action(
        subtests,
        StripJsComments(),
        valid_values=["x = 1 // note\n", "// only\nx = 1\n", "a/**/b", "x = 'http://a'\n", ""],
        expected_outputs=["x = 1\n", "x = 1\n", "a b", "x = 'http://a'\n", ""],
        invalid_values=[5, None, b"x = 1"],
        expected_exception_type=ValidationError,
        expected_input_type=str,
        expected_output_type=str,
        verbose=False,
    )


def test_is_an_action() -> None:
    assert isinstance(StripJsComments(), Action)


def test_the_class_has_the_agreed_name() -> None:
    assert type(StripJsComments()).__name__ == "StripJsComments"


@pytest.mark.parametrize("text", SAMPLES)
def test_does_what_the_function_does(text) -> None:
    assert StripJsComments()(text) == strip_js_comments(text)


def test_a_text_that_is_not_valid_javascript_is_not_a_card() -> None:
    """The scanner has no syntax it refuses."""
    assert isinstance(StripJsComments()("x = (\n// c"), str)


def test_it_has_no_options() -> None:
    with pytest.raises(TypeError):
        StripJsComments(on_error="keep")  # type: ignore[call-arg]


def test_two_actions_chain_with_the_right_shift() -> None:
    chained = StripJsComments() >> RemoveJsImports()
    assert isinstance(chained, Action)
    text = 'import a from "a" // the a\nrun(a) // go\n'
    assert chained(text) == remove_js_imports(strip_js_comments(text))
    assert chained(text) == "run(a)\n"
