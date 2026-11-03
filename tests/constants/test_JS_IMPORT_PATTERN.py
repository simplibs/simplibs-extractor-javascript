import re
import time
import pytest
from simplibs.extractor_javascript.constants import JS_IMPORT_PATTERN as PATTERN


def _found(text: str) -> list[str]:
    return [match.group(0) for match in PATTERN.finditer(text)]


def test_is_a_compiled_pattern() -> None:
    assert isinstance(PATTERN, re.Pattern)


@pytest.mark.parametrize(
    "line",
    [
        'import x from "m"',
        "import x from 'm'",
        'import x from "m";',
        'import { a, b as c } from "m"',
        'import * as ns from "m"',
        'import "m"',
        "import 'side-effect';",
        'import type { T } from "m"',
        'import { "name" as x } from "m"',
        'import def, { a } from "m"',
        'import def, * as ns from "m"',
        'import x from "./a/b.js"',
        'import"m"',
        'import{a}from"m"',
        '    import x from "m"',
        'import x from "m";   ',
    ],
    ids=[
        "default", "single-quotes", "semicolon", "named", "namespace", "bare", "bare-semicolon", "type", "string-name",
        "default-and-named", "default-and-namespace", "path", "no-space-bare", "no-spaces", "indented", "trailing-blanks",
    ],
)
def test_a_whole_statement_is_taken_with_its_indentation(line) -> None:
    assert _found(line) == [line]


def test_a_statement_over_several_lines() -> None:
    text = 'import {\n  a,\n  b as c,\n} from "m";\nconst x = 1\n'
    assert _found(text) == ['import {\n  a,\n  b as c,\n} from "m";']


def test_a_semicolon_on_the_next_line_belongs_to_the_statement() -> None:
    assert _found('import x from "m"\n;\nconst y = 1\n') == ['import x from "m"\n;']


def test_the_line_break_is_not_part_of_the_match() -> None:
    assert _found('import x from "m"\nconst y = 1\n') == ['import x from "m"']


def test_several_statements_are_all_found_and_the_code_between_stays() -> None:
    text = 'import a from "a"\nimport { b } from "b";\n\nconst x = a + b\nimport "c"\n'
    assert _found(text) == ['import a from "a"', 'import { b } from "b";', 'import "c"']


@pytest.mark.parametrize(
    "text",
    [
        'import("m")',
        'import("m").then(f)',
        'import ("m")',
        'const m = await import("m")',
        'import x from "m"; foo()',
        'import x from "m" // note',
        'import x from "m" /* note */',
        "import x from m",
        "import.meta.url",
        "important = 1",
        "imports.x = 1",
        "import = 1",
        '// import x from "m"',
        ' * import x from "m"',
        'const s = "import x from \'m\'"',
        'export { x } from "m"',
    ],
    ids=[
        "dynamic", "dynamic-chained", "dynamic-with-space", "dynamic-in-expression", "code-after", "line-comment-after", "block-comment-after",
        "no-quotes", "meta", "longer-word", "member", "assignment", "comment", "doc-comment", "string", "re-export",
    ],
)
def test_an_expression_and_a_statement_that_shares_its_line_is_left(text) -> None:
    assert _found(text) == []


def test_a_dynamic_import_next_to_a_static_one() -> None:
    text = 'import a from "a"\nconst lazy = () => import("./lazy")\n'
    assert _found(text) == ['import a from "a"']


def test_a_malformed_import_is_answered_in_reasonable_time() -> None:
    """The lazy part must not backtrack without end on a long line that has no module string."""
    text = "import " + "a, " * 3000 + "b\n"
    started = time.perf_counter()
    assert _found(text) == []
    assert time.perf_counter() - started < 5
