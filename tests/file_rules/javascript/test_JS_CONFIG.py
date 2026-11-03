from pathlib import Path
import pytest
from simplibs.rules.testing import assert_rule_contract
from simplibs.extractor_javascript.constants import JS_CONFIG_NAMES
from simplibs.extractor_javascript.file_rules import JS_CONFIG

VALID = ["package.json", "pkg/tsconfig.json", "next.config.js", "a/b/vite.config.ts", "yarn.lock", ".prettierrc", ".eslintrc.js"]
INVALID = [
    "a.js",
    "src/config.js",
    "package.json.bak",
    "tsconfig.base.json",
    "my.eslintrc.js",
    "mypackage.json",
    "package.json/a.js",
    "src/App.tsx",
]


def test_rule_contract(subtests) -> None:
    assert_rule_contract(
        subtests,
        JS_CONFIG,
        valid_values=[Path(path) for path in VALID],
        invalid_values=[Path(path) for path in INVALID],
        check_slots=False,
        check_value=False,
        verbose=False,
    )


@pytest.mark.parametrize("name", JS_CONFIG_NAMES)
def test_every_name_of_the_constant_is_configuration(name) -> None:
    assert JS_CONFIG(Path(name)) is True
    assert JS_CONFIG(Path("pkg") / name) is True


@pytest.mark.parametrize("path", INVALID)
def test_only_a_whole_name_counts(path) -> None:
    assert JS_CONFIG(Path(path)) is False
