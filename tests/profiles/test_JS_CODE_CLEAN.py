from simplibs.extractor import Profile
from simplibs.extractor.logic import apply_steps
from simplibs.extractor.testing import assert_profile
from simplibs.extractor_javascript.constants import JS_SUFFIXES
from simplibs.extractor_javascript.file_rules import JS_BASE
from simplibs.extractor_javascript.presets import JS_CLEAN
from simplibs.extractor_javascript.profiles import JS_CODE_CLEAN


def test_is_a_profile() -> None:
    assert isinstance(JS_CODE_CLEAN, Profile)


def test_profile_contract(subtests) -> None:
    assert_profile(
        subtests,
        JS_CODE_CLEAN,
        expected_key="javascript/code-clean",
        expected_output_name="javascript_code_clean.md",
        expected_format="markdown",
        included=(
            "a.js",
            "src/App.tsx",
            "src/c.jsx",
            "src/index.ts",
            "pages/_app.tsx",
            "src/a.mjs",
            "src/b.cjs",
            "types.d.ts",
            "src/a.test.js",
        ),
        excluded=(
            "README.md",
            "a.json",
            "a.css",
            "package.json",
            ".hidden.js",
            "src/.eslintrc.js",
            "a.py",
            "src/a.js.map",
        ),
        unchanged_suffixes=(".md", ".json", ".css", ".py", ".map"),
        verbose=False,
    )


def test_it_uses_the_base_rule_and_excludes_nothing_more() -> None:
    assert JS_CODE_CLEAN.include is JS_BASE
    assert JS_CODE_CLEAN.exclude is None


def test_every_javascript_suffix_has_steps() -> None:
    assert set(JS_CODE_CLEAN.steps) == set(JS_SUFFIXES)


def test_every_suffix_uses_the_clean_preset() -> None:
    assert all(JS_CODE_CLEAN.steps[suffix] is JS_CLEAN for suffix in JS_SUFFIXES)


def test_a_file_is_cleaned() -> None:
    for suffix in JS_SUFFIXES:
        result = JS_CODE_CLEAN.steps[suffix]("import a from 'a'\nconst x = a // c\nexport { x }\n")
        assert "// c" not in result
        assert "import a from 'a'" in result
        assert "export { x }" in result


def test_a_suffix_in_capitals_gets_the_same_cleaning() -> None:
    """The base rule takes `A.JS` too, so the step must be found for it."""
    assert "// c" not in apply_steps("x = 1 // c\n", JS_CODE_CLEAN.steps, ".JS")


def test_a_file_that_is_not_valid_javascript_does_not_fail() -> None:
    assert isinstance(JS_CODE_CLEAN.steps[".js"]("x = (\n// c"), str)
