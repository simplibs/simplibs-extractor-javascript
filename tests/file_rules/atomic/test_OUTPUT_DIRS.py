from pathlib import Path
import pytest
from simplibs.rules.testing import assert_rule_contract
from simplibs.extractor_javascript.constants import JS_OUTPUT_DIR_NAMES
from simplibs.extractor_javascript.file_rules import OUTPUT_DIRS

VALID = ["build/a.js", "dist/pkg/a.js", "pkg/out/a.js", ".next/server/pages/a.js", "a/b/build/c/d.js"]
INVALID = ["a.js", "src/a.js", "building/a.js", "distribution/a.js", "outer/a.js", "build.js", "pkg/dist.js", "output/a.js", "next/a.js"]


def test_rule_contract(subtests) -> None:
    assert_rule_contract(
        subtests,
        OUTPUT_DIRS,
        valid_values=[Path(path) for path in VALID],
        invalid_values=[Path(path) for path in INVALID],
        check_slots=False,
        check_value=False,
        verbose=False,
    )


@pytest.mark.parametrize("name", JS_OUTPUT_DIR_NAMES)
def test_every_name_of_the_constant_is_a_build_folder(name) -> None:
    assert OUTPUT_DIRS(Path(name) / "a.js") is True
    assert OUTPUT_DIRS(Path("pkg") / name / "deep" / "a.js") is True


@pytest.mark.parametrize("path", INVALID)
def test_a_folder_name_is_compared_as_a_whole(path) -> None:
    """`building` is not `build`, `next` is not `.next`, and a FILE called `build.js` is not a folder."""
    assert OUTPUT_DIRS(Path(path)) is False


def test_the_build_folder_of_next_js_is_taken_although_it_starts_with_a_dot() -> None:
    assert OUTPUT_DIRS(Path(".next/server/a.js")) is True
