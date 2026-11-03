import re
import pytest
from simplibs.extractor_javascript.constants import JS_EXPORT_KEYWORD_PATTERN as PATTERN


def _keyword(text: str) -> str | None:
    match = PATTERN.search(text)
    return None if match is None else match.group(0)


def test_is_a_compiled_pattern() -> None:
    assert isinstance(PATTERN, re.Pattern)


@pytest.mark.parametrize(
    "text, expected",
    [
        ("export function f() {}", "export "),
        ("export async function f() {}", "export "),
        ("export function* gen() {}", "export "),
        ("export class A {}", "export "),
        ("export abstract class A {}", "export "),
        ("export const a = 1", "export "),
        ("export let a = 1", "export "),
        ("export var a = 1", "export "),
        ("export interface Props {}", "export "),
        ("export type T = string", "export "),
        ("export enum E { A }", "export "),
        ("export declare const x: number", "export "),
        ("export default function App() {}", "export default "),
        ("export default async function App() {}", "export default "),
        ("export default function* gen() {}", "export default "),
        ("export default class App {}", "export default "),
        ("export default class App extends Base {}", "export default "),
    ],
    ids=[
        "function", "async-function", "generator", "class", "abstract-class", "const", "let", "var", "interface", "type",
        "enum", "declare", "default-function", "default-async-function", "default-generator", "default-class",
        "default-class-extends",
    ],
)
def test_the_keyword_in_front_of_a_named_declaration_is_matched(text, expected) -> None:
    assert _keyword(text) == expected


def test_the_declaration_itself_is_not_part_of_the_match() -> None:
    text = "export function f() {}"
    assert text[PATTERN.search(text).end():] == "function f() {}"


def test_the_indentation_is_group_one_and_stays() -> None:
    match = PATTERN.search("    export const a = 1")
    assert match.group(1) == "    "
    assert match.group(0) == "    export "


def test_it_is_found_on_any_line_of_a_text() -> None:
    text = "const x = 1\nexport const a = 2\nexport default function App() {}\n"
    assert [match.group(0) for match in PATTERN.finditer(text)] == ["export ", "export default "]


@pytest.mark.parametrize(
    "text",
    [
        "export default function () {}",
        "export default class extends Base {}",
        "export default () => {}",
        "export default async () => {}",
        "export default App;",
        "export default 42",
        "export default {}",
        "export { a, b }",
        'export * from "m"',
        "exports.a = 1",
        "exporter = 1",
        "// export const a = 1",
        "const s = 'export const a = 1'",
    ],
    ids=[
        "anonymous-function", "anonymous-class", "arrow", "async-arrow", "name", "number", "object", "list", "star",
        "commonjs", "other-word", "comment", "string",
    ],
)
def test_an_anonymous_default_and_everything_else_is_left(text) -> None:
    """Without `export default` an anonymous declaration would not be a valid statement."""
    assert _keyword(text) is None
