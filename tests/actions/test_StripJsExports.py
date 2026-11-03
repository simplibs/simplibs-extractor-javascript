import pytest
from simplibs.actions import Action
from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.extractor_javascript.actions import StripJsExports
from simplibs.extractor_javascript.logic import strip_js_exports

SAMPLES = [
    "export const a = 1\n",
    "export function f() {}\nexport default App\n",
    "export default function App() {}\n",
    "export { a, b };\nconst x = 1\n",
    "export * from 'm'\nexport * as ns from 'n'\n",
    "export default () => {}\n",
    "const s = `\nexport const a = 1\n`;\n",
    "",
]


def test_the_action_contract(subtests) -> None:
    assert_action(
        subtests,
        StripJsExports(),
        valid_values=["export const a = 1\n", "export { a }\nx = 1\n", "export default App;\n", "export default () => {}\n", ""],
        expected_outputs=["const a = 1\n", "x = 1\n", "", "export default () => {}\n", ""],
        invalid_values=[5, None, b"export const a = 1"],
        expected_exception_type=ValidationError,
        expected_input_type=str,
        expected_output_type=str,
        verbose=False,
    )


def test_is_an_action() -> None:
    assert isinstance(StripJsExports(), Action)


def test_the_class_has_the_agreed_name() -> None:
    assert type(StripJsExports()).__name__ == "StripJsExports"


@pytest.mark.parametrize("text", SAMPLES)
def test_does_what_the_function_does(text) -> None:
    assert StripJsExports()(text) == strip_js_exports(text)


def test_a_text_that_is_not_valid_javascript_is_not_a_card() -> None:
    assert isinstance(StripJsExports()("export {"), str)


def test_it_has_no_options() -> None:
    with pytest.raises(TypeError):
        StripJsExports(on_error="keep")  # type: ignore[call-arg]
