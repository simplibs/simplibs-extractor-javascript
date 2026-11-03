from pathlib import Path
import pytest
from simplibs.rules.testing import assert_rule_contract
from simplibs.extractor_javascript.constants import JS_TEST_DIR_NAMES
from simplibs.extractor_javascript.file_rules import JS_TESTS

BY_NAME = [
    "a.test.js",
    "App.test.tsx",
    "a.spec.ts",
    "a.tests.js",
    "a.specs.js",
    "test-utils.js",
    "test_helper.js",
    "a_test.js",
    "a-spec.js",
    "test.js",
    "spec.js",
    "src/a.test.js",
    "a.test.js.snap",
]
BY_FOLDER = [
    "__tests__/a.js",
    "src/__mocks__/b.js",
    "e2e/a.js",
    "tests/a.js",
    "test/a.js",
    "coverage/lcov.js",
    "pkg/coverage/a.js",
    "a/b/__tests__/c/d.js",
]
INVALID = [
    "a.js",
    "src/App.tsx",
    "latest.js",
    "contest.tsx",
    "inspector.ts",
    "attest.js",
    "testing.js",
    "specific.js",
    "respect.js",
    "protest.js",
    "tester.js",
    "src/testament/a.js",
    "src/latest/a.js",
    "src/contest/a.js",
]


def test_rule_contract(subtests) -> None:
    assert_rule_contract(
        subtests,
        JS_TESTS,
        valid_values=[Path(path) for path in [*BY_NAME, *BY_FOLDER]],
        invalid_values=[Path(path) for path in INVALID],
        check_slots=False,
        check_value=False,
        verbose=False,
    )


@pytest.mark.parametrize("path", BY_NAME)
def test_a_test_is_recognised_by_its_name(path) -> None:
    assert JS_TESTS(Path(path)) is True


@pytest.mark.parametrize("path", BY_FOLDER)
def test_a_test_is_recognised_by_its_folder(path) -> None:
    assert JS_TESTS(Path(path)) is True


@pytest.mark.parametrize("name", JS_TEST_DIR_NAMES)
def test_every_folder_name_of_the_constant_counts(name) -> None:
    assert JS_TESTS(Path(name) / "a.js") is True


@pytest.mark.parametrize("path", INVALID)
def test_the_word_must_stand_alone_in_the_name(path) -> None:
    """`test` or `spec` (and an optional `s`) at the start or after `.`, `-`, `_`, and before one of them or the end."""
    assert JS_TESTS(Path(path)) is False


@pytest.mark.parametrize("path", ["latest.js", "contest.tsx", "inspector.ts"])
def test_the_files_the_old_rule_would_throw_away_stay(path) -> None:
    assert JS_TESTS(Path(path)) is False
