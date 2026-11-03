import pytest
from simplibs.actions import Action
from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.extractor_javascript.actions import RemoveJsRequires
from simplibs.extractor_javascript.logic import remove_js_requires

SAMPLES = [
    'const fs = require("fs")\nrun()\n',
    "const { a, b } = require('m');\nrun()\n",
    'const a = require("a")\nconst b = require("b")\nrun(a, b)\n',
    'var get = require("m").get\nrun()\n',
    'const x = require(name)\n',
    'const s = `\nconst a = require("a")\n`;\n',
    "",
]


def test_the_action_contract(subtests) -> None:
    assert_action(
        subtests,
        RemoveJsRequires(),
        valid_values=['const fs = require("fs")\nrun()\n', "const x = require(name)\n", "x = 1\n", ""],
        expected_outputs=["run()\n", "const x = require(name)\n", "x = 1\n", ""],
        invalid_values=[5, None, b'const a = require("a")'],
        expected_exception_type=ValidationError,
        expected_input_type=str,
        expected_output_type=str,
        verbose=False,
    )


def test_is_an_action() -> None:
    assert isinstance(RemoveJsRequires(), Action)


def test_the_class_has_the_agreed_name() -> None:
    assert type(RemoveJsRequires()).__name__ == "RemoveJsRequires"


@pytest.mark.parametrize("text", SAMPLES)
def test_does_what_the_function_does(text) -> None:
    assert RemoveJsRequires()(text) == remove_js_requires(text)


def test_a_text_that_is_not_valid_javascript_is_not_a_card() -> None:
    assert isinstance(RemoveJsRequires()("const a = require("), str)


def test_it_has_no_options() -> None:
    with pytest.raises(TypeError):
        RemoveJsRequires(on_error="keep")  # type: ignore[call-arg]
