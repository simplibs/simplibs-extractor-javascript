import re
import pytest
from simplibs.extractor_javascript.constants import JS_EXPORT_LIST_PATTERN as PATTERN


def _found(text: str) -> list[str]:
    return [match.group(0) for match in PATTERN.finditer(text)]


def test_is_a_compiled_pattern() -> None:
    assert isinstance(PATTERN, re.Pattern)


@pytest.mark.parametrize(
    "line",
    [
        "export { a, b }",
        "export { a, b };",
        "export {}",
        "export { a as b }",
        'export { a as b } from "m"',
        "export { default } from './x'",
        'export * from "m"',
        "export * from 'm';",
        'export * as ns from "m"',
        "export type { T }",
        'export type { T } from "m"',
        'export type * from "m"',
        "export{a}",
        "  export { a };",
        "export { a };   ",
    ],
    ids=[
        "list", "list-semicolon", "empty", "alias", "alias-from", "default-from", "star", "star-single-quotes",
        "star-as", "type", "type-from", "type-star", "no-spaces", "indented", "trailing-blanks",
    ],
)
def test_an_export_that_only_names_things_is_taken_whole(line) -> None:
    assert _found(line) == [line]


def test_a_list_over_several_lines() -> None:
    text = "export {\n  a,\n  b,\n};\n"
    assert _found(text) == ["export {\n  a,\n  b,\n};"]


def test_the_line_break_is_not_part_of_the_match() -> None:
    assert _found('export * from "m"\nconst x = 1\n') == ['export * from "m"']


@pytest.mark.parametrize(
    "text",
    [
        "export const a = 1",
        "export default App",
        "export function f() {}",
        'export { a } from "m" // note',
        "export { a }; foo()",
        "export * from m",
        "exportx { a }",
        "// export { a }",
        "x = 1; export { a }",
    ],
    ids=["const", "default", "function", "comment-after", "code-after", "no-quotes", "other-word", "comment", "after-code"],
)
def test_anything_else_is_left(text) -> None:
    assert _found(text) == []
