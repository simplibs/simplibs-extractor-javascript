from pathlib import Path
import pytest
from simplibs.rules.testing import assert_rule_contract
from simplibs.extractor_javascript.constants import JS_ASSET_DIR_NAMES
from simplibs.extractor_javascript.file_rules import JS_ASSET_DIRS

VALID = ["public/a.js", "static/x.js", "src/assets/a.js", "a/b/public/c/d.js"]
INVALID = ["a.js", "src/a.js", "publication/a.js", "public.js", "assets.js", "my-assets/a.js", "asset/a.js"]


def test_rule_contract(subtests) -> None:
    assert_rule_contract(
        subtests,
        JS_ASSET_DIRS,
        valid_values=[Path(path) for path in VALID],
        invalid_values=[Path(path) for path in INVALID],
        check_slots=False,
        check_value=False,
        verbose=False,
    )


@pytest.mark.parametrize("name", JS_ASSET_DIR_NAMES)
def test_every_name_of_the_constant_is_a_folder_of_served_files(name) -> None:
    assert JS_ASSET_DIRS(Path(name) / "a.js") is True
    assert JS_ASSET_DIRS(Path("src") / name / "deep" / "a.js") is True


@pytest.mark.parametrize("path", INVALID)
def test_a_folder_name_is_compared_as_a_whole(path) -> None:
    assert JS_ASSET_DIRS(Path(path)) is False
