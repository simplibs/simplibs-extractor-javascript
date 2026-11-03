import pytest
from simplibs.actions import Action
from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.extractor_javascript.actions import RemoveJsImports
from simplibs.extractor_javascript.logic import remove_js_imports

SAMPLES = [
    'import a from "a"\nconst x = 1\n',
    "import a from 'a';\nimport { b } from 'b';\n\nconst x = a + b\n",
    'import {\n  a,\n  b as c,\n} from "m";\nrun(a, c)\n',
    'import type { T } from "m"\nlet x: T\n',
    'const lazy = () => import("./lazy")\n',
    'const s = `\nimport a from "a"\n`;\n',
    "",
]


def test_the_action_contract(subtests) -> None:
    assert_action(
        subtests,
        RemoveJsImports(),
        valid_values=["import a from 'a'\nx = 1\n", 'import "m"\nrun()\n', 'const lazy = import("m")\n', "x = 1\n", ""],
        expected_outputs=["x = 1\n", "run()\n", 'const lazy = import("m")\n', "x = 1\n", ""],
        invalid_values=[5, None, b"import a from 'a'"],
        expected_exception_type=ValidationError,
        expected_input_type=str,
        expected_output_type=str,
        verbose=False,
    )


def test_is_an_action() -> None:
    assert isinstance(RemoveJsImports(), Action)


def test_the_class_has_the_agreed_name() -> None:
    assert type(RemoveJsImports()).__name__ == "RemoveJsImports"


@pytest.mark.parametrize("text", SAMPLES)
def test_does_what_the_function_does(text) -> None:
    assert RemoveJsImports()(text) == remove_js_imports(text)


def test_a_text_that_is_not_valid_javascript_is_not_a_card() -> None:
    assert isinstance(RemoveJsImports()("import a from ("), str)


def test_it_has_no_options() -> None:
    with pytest.raises(TypeError):
        RemoveJsImports(on_error="keep")  # type: ignore[call-arg]
