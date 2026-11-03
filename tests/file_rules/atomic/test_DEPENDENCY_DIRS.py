from pathlib import Path
import pytest
from simplibs.rules.testing import assert_rule_contract
from simplibs.extractor_javascript.constants import JS_DEPENDENCY_DIR_NAMES
from simplibs.extractor_javascript.file_rules import DEPENDENCY_DIRS

VALID = ["node_modules/a.js", "pkg/node_modules/x/index.js", "a/b/node_modules/c.js", "node_modules/@scope/pkg/a.js"]
INVALID = ["a.js", "src/a.js", "node_modules.js", "my_node_modules/a.js", "node-modules/a.js", "modules/a.js", "src/node_modules_backup/a.js"]


def test_rule_contract(subtests) -> None:
    assert_rule_contract(
        subtests,
        DEPENDENCY_DIRS,
        valid_values=[Path(path) for path in VALID],
        invalid_values=[Path(path) for path in INVALID],
        check_slots=False,
        check_value=False,
        verbose=False,
    )


@pytest.mark.parametrize("name", JS_DEPENDENCY_DIR_NAMES)
def test_every_name_of_the_constant_is_a_folder_of_installed_packages(name) -> None:
    assert DEPENDENCY_DIRS(Path(name) / "a.js") is True
    assert DEPENDENCY_DIRS(Path("pkg") / name / "deep" / "a.js") is True


@pytest.mark.parametrize("path", INVALID)
def test_a_folder_name_is_compared_as_a_whole(path) -> None:
    assert DEPENDENCY_DIRS(Path(path)) is False
