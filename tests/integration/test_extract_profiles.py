import pytest
from simplibs.extractor import extract
from simplibs.extractor_javascript.profiles import JS_PROFILES

ALL_JS_FILES = {"src/index.ts", "src/app.tsx", "src/util.js", "src/app.test.ts", "src/types.d.ts"}
SOURCE_ONLY = {"src/index.ts", "src/app.tsx", "src/util.js"}

# profile key -> (file name of the output, texts that must be in it, texts that must not be)
CASES = {
    "javascript/code-clean": (
        "javascript_code_clean.md",
        [
            "import React from 'react';",
            "export function run()",
            "export default run;",
            "const fs = require('fs');",
            "http://x.com",
            "{}",
            "export interface Props",
            "test('run'",
        ],
        ["// start", "// inner note", "// tail", "/* note */", "The app."],
    ),
    "javascript/src-clean": (
        "javascript_src_clean.md",
        [
            "import React from 'react';",
            "export function run()",
            "export default run;",
            "const fs = require('fs');",
            "http://x.com",
            "{}",
            "import { run } from './app';",
        ],
        ["// start", "// inner note", "// tail", "/* note */", "The app.", "export interface Props", "test('run'"],
    ),
    "javascript/code-no-imports": (
        "javascript_code_no_imports.md",
        ["function run()", "http://x.com", "{}", "module.exports = { read", "run();", "test('run'", "interface Props"],
        [
            "import React",
            "import { run }",
            "require('fs')",
            "export function",
            "export default",
            "export interface",
            "// start",
            "// inner note",
            "/* note */",
        ],
    ),
    "javascript/data-all": (
        "javascript_data_all.md",
        [
            "import React from 'react';",
            "// start",
            "// inner note",
            "// tail",
            "/* note */",
            "The app.",
            "const fs = require('fs');",
            "export default run;",
            "export interface Props",
        ],
        [],
    ),
}


def _output(result) -> str:
    return result.target.read_text(encoding="utf-8")


def _ok(result) -> set[str]:
    return {report.relative for report in result.ok_files}


def test_the_cases_cover_every_profile_of_the_add_on() -> None:
    assert set(CASES) == {profile.key for profile in JS_PROFILES}


@pytest.mark.parametrize("key", sorted(CASES))
def test_a_profile_runs_and_writes_its_output(registered, project, key) -> None:
    file_name = CASES[key][0]
    result = extract(source=project, profile=key)
    assert result.success
    assert result.written
    assert result.profile_key == key
    assert result.target == project / file_name
    assert (project / file_name).is_file()
    assert result.tokens_estimate > 0


@pytest.mark.parametrize("key", sorted(CASES))
def test_the_output_has_what_the_profile_keeps_and_lacks_what_it_removes(registered, project, key) -> None:
    present, absent = CASES[key][1], CASES[key][2]
    text = _output(extract(source=project, profile=key))
    for fragment in present:
        assert fragment in text, f"{key}: expected {fragment!r} in the output"
    for fragment in absent:
        assert fragment not in text, f"{key}: did not expect {fragment!r} in the output"


@pytest.mark.parametrize("key", ["javascript/code-clean", "javascript/code-no-imports", "javascript/data-all"])
def test_these_profiles_take_every_javascript_and_typescript_file(registered, project, key) -> None:
    ok = _ok(extract(source=project, profile=key))
    assert ALL_JS_FILES <= ok
    assert not any(name.endswith((".md", ".txt", ".json")) for name in ok)


def test_src_clean_leaves_out_the_tests_and_the_declarations(registered, project) -> None:
    assert _ok(extract(source=project, profile="javascript/src-clean")) == SOURCE_ONLY


def test_the_output_of_a_run_is_not_read_by_the_next_run(registered, project) -> None:
    first = extract(source=project, profile="javascript/code-clean")
    second = extract(source=project, profile="javascript/code-clean")
    assert second.success
    assert _ok(second) == _ok(first)
    assert _output(second) == _output(first)


@pytest.mark.parametrize("key", ["javascript/code-clean", "javascript/src-clean", "javascript/code-no-imports"])
def test_a_profile_that_changes_the_text_makes_it_smaller(registered, project, key) -> None:
    result = extract(source=project, profile=key)
    reports = [report for report in result.ok_files if report.relative == "src/app.tsx"]
    assert reports and reports[0].bytes_out < reports[0].bytes_in
    assert all(report.bytes_out <= report.bytes_in for report in result.ok_files)


def test_data_all_changes_nothing(registered, project) -> None:
    result = extract(source=project, profile="javascript/data-all")
    assert all(report.bytes_out == report.bytes_in for report in result.ok_files)


def test_a_dry_run_plans_and_writes_nothing(registered, project) -> None:
    result = extract(source=project, profile="javascript/code-clean", dry_run=True)
    assert result.dry_run and not result.written
    assert not (project / "javascript_code_clean.md").exists()
    assert _ok(result) == ALL_JS_FILES | _ok(result)
    assert ALL_JS_FILES <= _ok(result)


def test_the_target_can_be_chosen(registered, project, tmp_path_factory) -> None:
    target = tmp_path_factory.mktemp("out") / "mine.md"
    result = extract(source=project, profile="javascript/src-clean", target=target)
    assert result.target == target
    assert target.is_file()


def test_wide_characters_survive_the_steps(registered, project) -> None:
    (project / "src" / "wide.js").write_text("const x = 'č€😀'; // čau\n", encoding="utf-8", newline="\n")
    text = _output(extract(source=project, profile="javascript/code-clean"))
    assert "'č€😀'" in text
    assert "čau" not in text


def test_a_suffix_in_capitals_is_read_and_cleaned_like_any_other(registered, project) -> None:
    (project / "src" / "Legacy.JS").write_text("var legacy = 1; // old\n", encoding="utf-8", newline="\n")
    result = extract(source=project, profile="javascript/code-clean")
    assert "src/Legacy.JS" in _ok(result)
    text = _output(result)
    assert "var legacy = 1;" in text
    assert "// old" not in text


def test_every_javascript_suffix_is_taken(registered, tmp_path) -> None:
    for suffix in (".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"):
        (tmp_path / f"a{suffix}").write_text("const a = 1 // c\n", encoding="utf-8", newline="\n")
    result = extract(source=tmp_path, profile="javascript/code-clean")
    assert _ok(result) == {f"a{suffix}" for suffix in (".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs")}
    assert "// c" not in _output(result)


# ---------------------------------------------------------------- text that is not valid JavaScript

@pytest.mark.parametrize("key", sorted(CASES))
def test_a_file_that_is_not_valid_javascript_is_no_error(registered, project, key) -> None:
    """The scanner has no syntax it refuses, so one broken file does not make a run fail."""
    (project / "src" / "broken.js").write_text("const x = (\n// c\n", encoding="utf-8", newline="\n")
    result = extract(source=project, profile=key)
    assert result.success
    assert result.error_files == ()
    assert "src/broken.js" in _ok(result)


def test_a_file_with_windows_line_endings_is_reported_either_way(registered, project) -> None:
    (project / "src" / "crlf.js").write_bytes(b"var x = 1; // c\r\nvar y = 2;\r\n")
    result = extract(source=project, profile="javascript/code-clean")
    assert "src/crlf.js" in {report.relative for report in result.files}
    assert ALL_JS_FILES <= _ok(result)
    assert result.written


def test_a_run_over_a_folder_without_javascript_files_writes_nothing(registered, tmp_path) -> None:
    (tmp_path / "notes.txt").write_text("hello\n", encoding="utf-8")
    result = extract(source=tmp_path, profile="javascript/code-clean")
    assert not result.written
    assert not result.success
    assert not (tmp_path / "javascript_code_clean.md").exists()
