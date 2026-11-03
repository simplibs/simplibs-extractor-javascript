from pathlib import Path
import pytest
from simplibs.rules.testing import assert_rule_contract
from simplibs.extractor_javascript.file_rules import UNDERSCORE_NAME

VALID = ["_app.tsx", "pages/_document.tsx", "_helpers.js", "src/_private/_a.js", "__a.js"]
INVALID = ["app.js", "my_app.js", "pages/a_.js", "_dir/a.js", "src/_private/a.js", "a.js"]


def test_rule_contract(subtests) -> None:
    assert_rule_contract(
        subtests,
        UNDERSCORE_NAME,
        valid_values=[Path(path) for path in VALID],
        invalid_values=[Path(path) for path in INVALID],
        check_slots=False,
        check_value=False,
        verbose=False,
    )


@pytest.mark.parametrize("path", VALID)
def test_a_name_that_starts_with_an_underscore_is_private(path) -> None:
    assert UNDERSCORE_NAME(Path(path)) is True


@pytest.mark.parametrize("path", INVALID)
def test_other_names_are_not(path) -> None:
    assert UNDERSCORE_NAME(Path(path)) is False


@pytest.mark.parametrize("path", ["_dir/a.js", "src/_private/a.js"])
def test_only_the_name_of_the_file_is_judged_not_its_folders(path) -> None:
    assert UNDERSCORE_NAME(Path(path)) is False
