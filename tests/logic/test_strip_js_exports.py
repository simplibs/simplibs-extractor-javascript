import pytest
from simplibs.exception import ValidationError
from simplibs.extractor_javascript.logic import strip_js_exports

SAMPLES = [
    "export const a = 1\n",
    "export function f() {}\nexport default App\n",
    "export default function App() {}\n",
    "export { a, b };\nconst x = 1\n",
    "export * from 'm'\nexport * as ns from 'n'\n",
    "export type { T }\nexport type U = string\n",
    "export default () => {}\n",
    "  export const indented = 1\n",
    "const s = `\nexport const a = 1\n`;\n",
    "",
]


@pytest.mark.parametrize(
    "text, expected",
    [
        ("export function f() {}\n", "function f() {}\n"),
        ("export async function f() {}\n", "async function f() {}\n"),
        ("export function* gen() {}\n", "function* gen() {}\n"),
        ("export class A {}\n", "class A {}\n"),
        ("export abstract class A {}\n", "abstract class A {}\n"),
        ("export const a = 1\n", "const a = 1\n"),
        ("export let a = 1\n", "let a = 1\n"),
        ("export var a = 1\n", "var a = 1\n"),
        ("export interface Props {}\n", "interface Props {}\n"),
        ("export type T = string\n", "type T = string\n"),
        ("export enum E { A }\n", "enum E { A }\n"),
        ("export declare const x: number\n", "declare const x: number\n"),
        ("export default function App() {}\n", "function App() {}\n"),
        ("export default async function App() {}\n", "async function App() {}\n"),
        ("export default class App {}\n", "class App {}\n"),
        ("export default class App extends Base {}\n", "class App extends Base {}\n"),
    ],
    ids=[
        "function", "async-function", "generator", "class", "abstract-class", "const", "let", "var", "interface", "type",
        "enum", "declare", "default-function", "default-async-function", "default-class", "default-class-extends",
    ],
)
def test_the_keyword_goes_and_the_declaration_stays(text, expected) -> None:
    assert strip_js_exports(text) == expected


def test_the_indentation_stays() -> None:
    assert strip_js_exports("  export const a = 1\n") == "  const a = 1\n"
    assert strip_js_exports("declare module 'm' {\n    export function f(): void\n}\n") == (
        "declare module 'm' {\n    function f(): void\n}\n"
    )


@pytest.mark.parametrize(
    "text, expected",
    [
        ("export { a, b }\nconst x = 1\n", "const x = 1\n"),
        ("export { a, b };\nconst x = 1\n", "const x = 1\n"),
        ("export {}\nconst x = 1\n", "const x = 1\n"),
        ("export { a as b } from 'm'\nconst x = 1\n", "const x = 1\n"),
        ("export * from 'm'\nconst x = 1\n", "const x = 1\n"),
        ("export * as ns from 'm'\nconst x = 1\n", "const x = 1\n"),
        ("export type { T }\nconst x = 1\n", "const x = 1\n"),
        ("export type { T } from 'm'\nconst x = 1\n", "const x = 1\n"),
        ("export {\n  a,\n  b,\n};\nconst x = 1\n", "const x = 1\n"),
        ("export default App;\nconst x = 1\n", "const x = 1\n"),
        ("export default App\nconst x = 1\n", "const x = 1\n"),
        ("const x = 1\nexport default App;\n", "const x = 1\n"),
        ("const x = 1\nexport { x }", "const x = 1"),
    ],
    ids=[
        "list", "list-semicolon", "empty-list", "alias-from", "star", "star-as", "type-list", "type-list-from", "several-lines",
        "default-name", "default-name-no-semicolon", "default-name-last", "list-last-without-newline",
    ],
)
def test_a_line_that_only_exports_goes_whole(text, expected) -> None:
    assert strip_js_exports(text) == expected


def test_a_module_of_only_exports_becomes_empty() -> None:
    assert strip_js_exports("export { a }\nexport default b;\nexport * from 'm'\n") == ""


@pytest.mark.parametrize(
    "text",
    [
        "export default function () {}\n",
        "export default class extends Base {}\n",
        "export default () => {}\n",
        "export default async () => {}\n",
        "export default { a: 1 }\n",
        "export default 42\n",
        "export default App.extend()\n",
        "exports.a = 1\n",
        "module.exports = { a }\n",
        "export { a }; run()\n",
    ],
    ids=[
        "anonymous-function", "anonymous-class", "arrow", "async-arrow", "object", "number", "call-chain", "commonjs-exports",
        "commonjs-module", "list-with-code-after",
    ],
)
def test_what_would_not_be_valid_without_its_keyword_or_is_not_an_export_stays(text) -> None:
    assert strip_js_exports(text) == text


def test_an_export_in_a_comment_or_a_template_stays() -> None:
    for text in (
        "/*\nexport const a = 1\n*/\n",
        "const s = `\nexport const a = 1\n`;\n",
        "const s = `\nexport { a }\n`;\n",
        "// export const a = 1\n",
        'const s = "export const a = 1"\n',
    ):
        assert strip_js_exports(text) == text


def test_a_whole_module() -> None:
    text = (
        "import a from 'a'\n"
        "\n"
        "export const VERSION = 1\n"
        "\n"
        "export function run() {\n"
        "  return a\n"
        "}\n"
        "\n"
        "export default run\n"
        "export { VERSION as V }\n"
    )
    expected = (
        "import a from 'a'\n"
        "\n"
        "const VERSION = 1\n"
        "\n"
        "function run() {\n"
        "  return a\n"
        "}\n"
    )
    # How many blank lines are left in front of the removed tail is the business of `remove_spans`.
    assert strip_js_exports(text).rstrip("\n") == expected.rstrip("\n")


def test_the_code_of_a_declaration_is_never_touched() -> None:
    text = "export const a = { export: 1 }\nexport function f() { return 'export const x' }\n"
    assert strip_js_exports(text) == "const a = { export: 1 }\nfunction f() { return 'export const x' }\n"


def test_a_text_without_exports_stays_as_it_is() -> None:
    text = "function f(a,b){\n  return  a+b\n}\n"
    assert strip_js_exports(text) == text


def test_an_empty_text_stays_empty() -> None:
    assert strip_js_exports("") == ""


# ---------------------------------------------------------------- guarantees

@pytest.mark.parametrize("text", SAMPLES)
def test_a_second_run_changes_nothing(text) -> None:
    once = strip_js_exports(text)
    assert strip_js_exports(once) == once


@pytest.mark.parametrize("text", SAMPLES)
def test_no_export_keyword_is_left_in_front_of_a_named_declaration(text) -> None:
    import re

    result = strip_js_exports(text)
    code = result.split("`")[0] if "`" in result else result
    assert not re.search(r"^[ \t]*export\s+(?:default\s+)?(?:async\s+)?(?:function|class|const|let|var|interface|enum)\s+\w", code, re.M)


@pytest.mark.parametrize("text", ["'", '"', "`", "/*", "//", "/", "${", "`${", "export", "export {", "export default", "export * from"])
def test_a_text_that_is_not_valid_javascript_never_raises(text) -> None:
    assert isinstance(strip_js_exports(text), str)


@pytest.mark.parametrize("value", [None, 5, b"export const a = 1", ["export const a = 1"]])
def test_the_text_must_be_a_str(value) -> None:
    with pytest.raises(ValidationError):
        strip_js_exports(value)
