from simplibs.extractor import Profile
from simplibs.extractor.logic import apply_steps
from simplibs.extractor.testing import assert_profile
from simplibs.extractor_javascript.constants import JS_SUFFIXES
from simplibs.extractor_javascript.file_rules import JS_BASE, JS_STRICT_EXCLUDE
from simplibs.extractor_javascript.presets import JS_CLEAN
from simplibs.extractor_javascript.profiles import JS_SRC_CLEAN


def test_is_a_profile() -> None:
    assert isinstance(JS_SRC_CLEAN, Profile)


def test_profile_contract(subtests) -> None:
    assert_profile(
        subtests,
        JS_SRC_CLEAN,
        expected_key="javascript/src-clean",
        expected_output_name="javascript_src_clean.md",
        expected_format="markdown",
        included=(
            "a.js",
            "src/App.tsx",
            "src/index.ts",
            "pages/_app.tsx",
            "src/types.ts",
            "latest.js",
            "contest.tsx",
            "src/components/Button.jsx",
        ),
        excluded=(
            "src/a.test.js",
            "src/App.spec.tsx",
            "__tests__/a.js",
            "e2e/a.js",
            "package.json",
            "pkg/vite.config.ts",
            "types.d.ts",
            "src/global.d.ts",
            "node_modules/x/index.js",
            "dist/a.js",
            ".next/server/a.js",
            "build/a.js",
            "public/a.js",
            "src/assets/a.js",
            ".git/hooks/a.js",
            "README.md",
            "a.json",
            ".hidden.js",
        ),
        unchanged_suffixes=(".md", ".json", ".css", ".py"),
        verbose=False,
    )


def test_it_uses_the_base_rule_and_the_strict_exclusion() -> None:
    assert JS_SRC_CLEAN.include is JS_BASE
    assert JS_SRC_CLEAN.exclude is JS_STRICT_EXCLUDE


def test_every_javascript_suffix_has_steps() -> None:
    assert set(JS_SRC_CLEAN.steps) == set(JS_SUFFIXES)


def test_every_suffix_uses_the_clean_preset() -> None:
    assert all(JS_SRC_CLEAN.steps[suffix] is JS_CLEAN for suffix in JS_SUFFIXES)


def test_a_file_is_cleaned() -> None:
    result = JS_SRC_CLEAN.steps[".tsx"]("import a from 'a'\nconst x = a // c\nexport { x }\n")
    assert "// c" not in result
    assert "import a from 'a'" in result
    assert "export { x }" in result


def test_a_suffix_in_capitals_gets_the_same_cleaning() -> None:
    assert "// c" not in apply_steps("x = 1 // c\n", JS_SRC_CLEAN.steps, ".JSX")
