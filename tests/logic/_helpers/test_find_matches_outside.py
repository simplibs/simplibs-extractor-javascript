from simplibs.extractor_javascript.constants import JS_IMPORT_PATTERN, JS_REQUIRE_PATTERN
from simplibs.extractor_javascript.logic._helpers import find_matches_outside, scan_js


def _found(text: str, pattern=JS_IMPORT_PATTERN) -> list[str]:
    return [match.group(0) for match in find_matches_outside(text, pattern, scan_js(text))]


def test_a_statement_in_the_code_is_found() -> None:
    assert _found('import a from "a"\nconst x = 1\n') == ['import a from "a"']


def test_returns_matches_in_the_order_of_the_text() -> None:
    text = 'import a from "a"\nconst x = 1\nimport b from "b"\n'
    assert _found(text) == ['import a from "a"', 'import b from "b"']


def test_a_text_without_matches_gives_an_empty_list() -> None:
    assert _found("const x = 1\n") == []
    assert find_matches_outside("", JS_IMPORT_PATTERN, scan_js("")) == []


def test_a_line_inside_a_block_comment_is_not_a_statement() -> None:
    assert _found('/*\nimport a from "a"\n*/\nconst x = 1\n') == []


def test_a_line_inside_a_template_literal_is_not_a_statement() -> None:
    assert _found('const sample = `\nimport a from "a"\n`;\n') == []


def test_an_indented_line_inside_a_template_literal_is_not_a_statement() -> None:
    assert _found('const sample = `\n    import a from "a"\n`;\n') == []


def test_a_statement_after_a_template_literal_is_found() -> None:
    text = 'const sample = `a`\nimport b from "b"\n'
    assert _found(text) == ['import b from "b"']


def test_a_statement_after_a_block_comment_on_a_line_of_its_own_is_found() -> None:
    text = '/* about b */\nimport b from "b"\n'
    assert _found(text) == ['import b from "b"']


def test_a_statement_between_two_protected_places_is_found() -> None:
    text = '/*\nimport a from "a"\n*/\nimport b from "b"\nconst s = `\nimport c from "c"\n`\n'
    assert _found(text) == ['import b from "b"']


def test_the_statements_and_the_protected_ones_together() -> None:
    text = 'import a from "a"\n/*\nimport b from "b"\n*/\nimport c from "c"\n'
    assert _found(text) == ['import a from "a"', 'import c from "c"']


def test_it_works_for_any_pattern_of_lines() -> None:
    text = 'const a = require("a")\nconst s = `\nconst b = require("b")\n`\nconst c = require("c")\n'
    assert _found(text, JS_REQUIRE_PATTERN) == ['const a = require("a")', 'const c = require("c")']


def test_the_matches_are_real_match_objects() -> None:
    text = 'import a from "a"\n'
    (match,) = find_matches_outside(text, JS_IMPORT_PATTERN, scan_js(text))
    assert match.start() == 0 and match.end() == len(text) - 1


def test_the_scan_decides_not_the_text() -> None:
    """With an empty scan nothing is protected, so even a line in a comment is found."""
    from simplibs.extractor_javascript.logic._helpers import JsScan

    text = '/*\nimport a from "a"\n*/\n'
    assert len(find_matches_outside(text, JS_IMPORT_PATTERN, JsScan((), (), ()))) == 1
