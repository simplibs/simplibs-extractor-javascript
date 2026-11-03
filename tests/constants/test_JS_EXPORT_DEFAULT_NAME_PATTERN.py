import re
import pytest
from simplibs.extractor_javascript.constants import JS_EXPORT_DEFAULT_NAME_PATTERN as PATTERN


def _found(text: str) -> list[str]:
    return [match.group(0) for match in PATTERN.finditer(text)]


def test_is_a_compiled_pattern() -> None:
    assert isinstance(PATTERN, re.Pattern)


@pytest.mark.parametrize(
    "line",
    [
        "export default App;",
        "export default App",
        "export default App ;",
        "export  default   App;",
        "  export default App;",
        "export default App;   ",
        "export default $store;",
        "export default _private",
        "export default App1;",
    ],
    ids=["semicolon", "no-semicolon", "space-before-semicolon", "many-spaces", "indented", "trailing-blanks", "dollar", "underscore", "digit"],
)
def test_a_default_export_that_only_names_something_is_taken_whole(line) -> None:
    assert _found(line) == [line]


def test_the_line_break_is_not_part_of_the_match() -> None:
    assert _found("export default App;\nconst x = 1\n") == ["export default App;"]


def test_a_name_without_a_semicolon_followed_by_a_new_statement_is_taken() -> None:
    assert _found("export default App\n\nconst x = 1\n") == ["export default App"]


@pytest.mark.parametrize(
    "text",
    [
        "export default function App() {}",
        "export default () => {}",
        "export default class App {}",
        "export default 42",
        "export default {}",
        'export default "text"',
        "export default App.extend()",
        "export default App,",
        "export default App; foo()",
        "export default async () => {}",
        "export App;",
        "default App;",
        "// export default App;",
    ],
    ids=[
        "function", "arrow", "class", "number", "object", "string", "call-chain", "comma", "more-code-after",
        "async-arrow", "no-default", "no-export", "comment",
    ],
)
def test_anything_that_carries_code_is_left(text) -> None:
    assert _found(text) == []


@pytest.mark.parametrize(
    "continuation",
    ["? a : b", ": b", ".x()", "(1)", "[0]", "`t`", "+ 1", "- 1", "* 2", "/ 2", "% 2", "< 2", "> 2", "= 2", "& 2", "| 2", ", 2"],
)
def test_a_name_that_the_next_line_goes_on_with_is_not_taken(continuation) -> None:
    """`export default FILE` followed by `? a : b` is a conditional expression, not a name."""
    assert _found(f"export default FILE\n{continuation}\n") == []


def test_two_default_exports_in_a_text_are_both_found() -> None:
    assert _found("export default A;\nx = 1\nexport default B\n") == ["export default A;", "export default B"]
