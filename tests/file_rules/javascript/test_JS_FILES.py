from pathlib import Path
import pytest
from simplibs.rules.testing import assert_rule_contract
from simplibs.extractor_javascript.constants import JS_SUFFIXES
from simplibs.extractor_javascript.file_rules import JS_FILES

VALID = ["a.js", "src/App.jsx", "a.ts", "src/App.tsx", "src/a.mjs", "src/b.cjs", "pkg/a.min.js", "types.d.ts", "A.JS", "App.TSX"]
INVALID = ["a.json", "a.css", "a.py", "a.js.map", "a.jsx.bak", "README.md", "a", "a.mdx", "a.html", "package.json"]


def test_rule_contract(subtests) -> None:
    assert_rule_contract(
        subtests,
        JS_FILES,
        valid_values=[Path(path) for path in VALID],
        invalid_values=[Path(path) for path in INVALID],
        check_slots=False,
        check_value=False,
        verbose=False,
    )


@pytest.mark.parametrize("suffix", JS_SUFFIXES)
def test_every_suffix_of_the_constant_is_taken(suffix) -> None:
    assert JS_FILES(Path("src") / f"a{suffix}") is True


@pytest.mark.parametrize("path", ["A.JS", "App.TSX", "a.Mjs"])
def test_the_suffix_is_compared_without_regard_to_case(path) -> None:
    assert JS_FILES(Path(path)) is True


@pytest.mark.parametrize("path", INVALID)
def test_anything_else_is_not_javascript(path) -> None:
    assert JS_FILES(Path(path)) is False


@pytest.mark.parametrize("path", ["src/App.jsx", "src/App.tsx"])
def test_react_files_belong_here_like_any_other(path) -> None:
    assert JS_FILES(Path(path)) is True
