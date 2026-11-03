from pathlib import Path
import pytest
from simplibs.rules.testing import assert_rule_contract
from simplibs.extractor_javascript.file_rules import JS_STRICT_EXCLUDE

TESTS = ["a.test.js", "src/App.spec.tsx", "__tests__/a.js", "e2e/a.js"]
CONFIG = ["package.json", "tsconfig.json", "pkg/vite.config.ts", "next.config.js"]
DECLARATIONS = ["types.d.ts", "src/global.d.ts"]
VCS = [".git/hooks/a.js", ".svn/a.js"]
DEPENDENCIES = ["node_modules/x/index.js", "pkg/node_modules/y/a.js"]
OUTPUT = ["dist/a.js", ".next/server/a.js", "build/a.js", "out/a.js"]
ASSETS = ["public/a.js", "static/x.js", "src/assets/a.js"]
PROJECT_CODE = [
    "a.js",
    "src/App.tsx",
    "src/index.ts",
    "pages/_app.tsx",
    "src/types.ts",
    "latest.js",
    "contest.tsx",
    "inspector.ts",
    "src/components/Button.jsx",
]


def test_rule_contract(subtests) -> None:
    assert_rule_contract(
        subtests,
        JS_STRICT_EXCLUDE,
        valid_values=[Path(path) for path in [*TESTS, *CONFIG, *DECLARATIONS, *VCS, *DEPENDENCIES, *OUTPUT, *ASSETS]],
        invalid_values=[Path(path) for path in PROJECT_CODE],
        check_slots=False,
        check_value=False,
        verbose=False,
    )


@pytest.mark.parametrize("path", TESTS)
def test_tests_are_excluded(path) -> None:
    assert JS_STRICT_EXCLUDE(Path(path)) is True


@pytest.mark.parametrize("path", CONFIG)
def test_configuration_is_excluded(path) -> None:
    assert JS_STRICT_EXCLUDE(Path(path)) is True


@pytest.mark.parametrize("path", DECLARATIONS)
def test_type_declarations_are_excluded(path) -> None:
    """A `.d.ts` file only describes the types of code that exists elsewhere."""
    assert JS_STRICT_EXCLUDE(Path(path)) is True


@pytest.mark.parametrize("path", VCS)
def test_version_control_is_excluded(path) -> None:
    assert JS_STRICT_EXCLUDE(Path(path)) is True


@pytest.mark.parametrize("path", DEPENDENCIES)
def test_installed_packages_are_excluded(path) -> None:
    assert JS_STRICT_EXCLUDE(Path(path)) is True


@pytest.mark.parametrize("path", OUTPUT)
def test_build_output_is_excluded(path) -> None:
    assert JS_STRICT_EXCLUDE(Path(path)) is True


@pytest.mark.parametrize("path", ASSETS)
def test_served_files_are_excluded(path) -> None:
    assert JS_STRICT_EXCLUDE(Path(path)) is True


@pytest.mark.parametrize("path", PROJECT_CODE)
def test_the_code_of_the_application_is_not(path) -> None:
    """Only what the application does stays; `index.*` and `_app.tsx` are part of it."""
    assert JS_STRICT_EXCLUDE(Path(path)) is False
