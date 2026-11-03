from pathlib import Path
import pytest
from simplibs.rules import Rule
from simplibs.rules.testing import assert_rule_contract
from simplibs.extractor_javascript.file_rules import JS_BASE, build_js_base

TAKEN = ["a.js", "src/App.tsx", "src/index.ts", "pages/_app.tsx", "src/a.mjs", "types.d.ts", "src/a.test.js"]
LEFT_OUT = ["a.json", "README.md", ".hidden.js", "src/.eslintrc.js", "a.py", "package.json"]


def test_is_a_rule() -> None:
    assert isinstance(JS_BASE, Rule)


def test_rule_contract(subtests) -> None:
    assert_rule_contract(
        subtests,
        JS_BASE,
        valid_values=[Path(path) for path in TAKEN],
        invalid_values=[Path(path) for path in LEFT_OUT],
        check_slots=False,
        check_value=False,
        verbose=False,
    )


@pytest.mark.parametrize("path", [*TAKEN, *LEFT_OUT])
def test_decides_like_the_builder_with_its_defaults(path) -> None:
    assert JS_BASE(Path(path)) is build_js_base()(Path(path))


def test_takes_index_and_underscore_files() -> None:
    assert JS_BASE(Path("src/index.tsx")) is True
    assert JS_BASE(Path("pages/_app.tsx")) is True
