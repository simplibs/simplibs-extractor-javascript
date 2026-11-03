import re
import time
import pytest
from simplibs.extractor_javascript.constants import JS_REQUIRE_PATTERN as PATTERN


def _found(text: str) -> list[str]:
    return [match.group(0) for match in PATTERN.finditer(text)]


def test_is_a_compiled_pattern() -> None:
    assert isinstance(PATTERN, re.Pattern)


@pytest.mark.parametrize(
    "line",
    [
        'const fs = require("fs")',
        "const fs = require('fs');",
        'let fs = require("fs")',
        'var fs = require("fs")',
        'const { a, b } = require("m")',
        'const { a, b: { c } } = require("m")',
        'const { a: { b: { c } } } = require("m")',
        'const [x] = require("m")',
        'const [x, y] = require("m")',
        'var get = require("m").get',
        'const x = require( "m" )',
        'const x=require("m")',
        '    const x = require("m")',
        'const x = require("m");   ',
        'const $el = require("m")',
    ],
    ids=[
        "const", "single-quotes-semicolon", "let", "var", "destructuring", "nested-destructuring", "two-levels",
        "array", "array-two", "member", "spaces-inside", "no-spaces", "indented", "trailing-blanks", "dollar-name",
    ],
)
def test_a_whole_commonjs_import_is_taken_with_its_indentation(line) -> None:
    assert _found(line) == [line]


def test_a_statement_with_a_semicolon_is_taken_whatever_follows() -> None:
    assert _found('const x = require("m");\n.call()\n') == ['const x = require("m");']


def test_a_semicolon_on_the_next_line_belongs_to_the_statement() -> None:
    assert _found('const x = require("m")\n;\n') == ['const x = require("m")\n;']


def test_a_statement_without_a_semicolon_is_taken_when_the_next_line_starts_a_new_one() -> None:
    assert _found('const a = require("a")\nconst b = 1\n') == ['const a = require("a")']


def test_the_line_break_is_not_part_of_the_match() -> None:
    assert _found('const a = require("a")\nfoo()\n') == ['const a = require("a")']


def test_several_requires_are_all_found_and_the_code_between_stays() -> None:
    text = 'const a = require("a")\nconst { b } = require("b");\n\nrun(a, b)\n'
    assert _found(text) == ['const a = require("a")', 'const { b } = require("b");']


@pytest.mark.parametrize(
    "continuation",
    [", b = require('b')", ".call()", "(1)", "[0]", "`t`", "+ 1", "- 1", "* 2", "/ 2", "% 2", "< 2", "> 2", "= 2", "& 2", "| 2", "? a : b", ": b"],
)
def test_a_declaration_that_the_next_line_goes_on_with_is_not_taken(continuation) -> None:
    """Removing the first line would leave a broken second one (comma-first style, a chained call, an operator)."""
    assert _found(f'var a = require("a")\n{continuation}\n') == []


@pytest.mark.parametrize(
    "text",
    [
        'const a = require("a"), b = require("b")',
        "const x = require(name)",
        'const x = require("a" + b)',
        'const x = require("m")()',
        'const x = require("m").a.b',
        'const x = require("m").default || y',
        'const x = await require("m")',
        'x = require("m")',
        'module.exports = require("m")',
        'export const x = require("m")',
        'const { a = 1 } = require("m")',
        'const { a: { b: { c: { d } } } } = require("m")',
        'const x = require("m") // note',
        '// const x = require("m")',
        "const x = require(`m`)",
        'const x = import("m")',
    ],
    ids=[
        "two-declarators", "not-a-string", "expression", "called", "two-members", "or-expression", "await", "no-declaration",
        "assignment", "exported", "default-value", "three-levels", "comment-after", "comment", "template", "dynamic-import",
    ],
)
def test_what_is_code_and_not_a_dependency_is_left(text) -> None:
    assert _found(text) == []


def test_a_malformed_destructuring_is_answered_in_reasonable_time() -> None:
    text = "const { " + "a, " * 3000 + "b = require('m')\n"
    started = time.perf_counter()
    assert _found(text) == []
    assert time.perf_counter() - started < 5
