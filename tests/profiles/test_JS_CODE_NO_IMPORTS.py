from simplibs.extractor import Profile
from simplibs.extractor.logic import apply_steps
from simplibs.extractor.testing import assert_profile
from simplibs.extractor_javascript.constants import JS_SUFFIXES
from simplibs.extractor_javascript.file_rules import JS_BASE
from simplibs.extractor_javascript.presets import JS_NO_IMPORTS
from simplibs.extractor_javascript.profiles import JS_CODE_NO_IMPORTS


def test_is_a_profile() -> None:
    assert isinstance(JS_CODE_NO_IMPORTS, Profile)


def test_profile_contract(subtests) -> None:
    assert_profile(
        subtests,
        JS_CODE_NO_IMPORTS,
        expected_key="javascript/code-no-imports",
        expected_output_name="javascript_code_no_imports.md",
        expected_format="markdown",
        included=("a.js", "src/App.tsx", "src/index.ts", "pages/_app.tsx", "src/a.mjs", "src/b.cjs", "src/a.test.js"),
        excluded=("README.md", "a.json", "a.css", "package.json", ".hidden.js", "a.py"),
        unchanged_suffixes=(".md", ".json", ".css", ".py"),
        verbose=False,
    )


def test_it_uses_the_base_rule_and_excludes_nothing_more() -> None:
    assert JS_CODE_NO_IMPORTS.include is JS_BASE
    assert JS_CODE_NO_IMPORTS.exclude is None


def test_every_javascript_suffix_has_steps() -> None:
    assert set(JS_CODE_NO_IMPORTS.steps) == set(JS_SUFFIXES)


def test_every_suffix_uses_the_no_imports_preset() -> None:
    assert all(JS_CODE_NO_IMPORTS.steps[suffix] is JS_NO_IMPORTS for suffix in JS_SUFFIXES)


def test_a_file_is_reduced_to_its_logic() -> None:
    text = "import a from 'a' // the a\n\nexport function f() {\n  return a // c\n}\n\nexport default f\n"
    for suffix in JS_SUFFIXES:
        assert JS_CODE_NO_IMPORTS.steps[suffix](text).strip("\n") == "function f() {\n  return a\n}"


def test_a_suffix_in_capitals_gets_the_same_reduction() -> None:
    assert apply_steps("import a from 'a'\nx = 1\n", JS_CODE_NO_IMPORTS.steps, ".TSX").strip("\n") == "x = 1"


def test_a_file_that_is_not_valid_javascript_does_not_fail() -> None:
    assert isinstance(JS_CODE_NO_IMPORTS.steps[".js"]("import a from (\n// c"), str)
