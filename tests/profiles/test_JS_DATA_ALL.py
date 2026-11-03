from simplibs.extractor import Profile
from simplibs.extractor.logic import apply_steps
from simplibs.extractor.testing import assert_profile
from simplibs.extractor_javascript.file_rules import JS_BASE
from simplibs.extractor_javascript.profiles import JS_DATA_ALL


def test_is_a_profile() -> None:
    assert isinstance(JS_DATA_ALL, Profile)


def test_profile_contract(subtests) -> None:
    assert_profile(
        subtests,
        JS_DATA_ALL,
        expected_key="javascript/data-all",
        expected_output_name="javascript_data_all.md",
        expected_format="markdown",
        included=("a.js", "src/App.tsx", "src/index.ts", "pages/_app.tsx", "src/a.mjs", "src/a.test.js", "types.d.ts"),
        excluded=("README.md", "a.json", "a.css", "package.json", ".hidden.js", "a.py"),
        step_cases={
            ".js": [("x = 1 // c\n", "x = 1 // c\n"), ("import a from 'a'\n", "import a from 'a'\n")],
            ".tsx": [("x = (\n", "x = (\n")],
        },
        unchanged_suffixes=(".md", ".json", ".css"),
        verbose=False,
    )


def test_it_uses_the_base_rule_and_excludes_nothing_more() -> None:
    assert JS_DATA_ALL.include is JS_BASE
    assert JS_DATA_ALL.exclude is None


def test_there_are_no_steps_at_all() -> None:
    assert JS_DATA_ALL.steps is None


def test_a_file_comes_out_exactly_as_it_is() -> None:
    text = "// header\r\nimport a from 'a'\r\nexport default a\r\n"
    assert apply_steps(text, JS_DATA_ALL.steps, ".js") == text
