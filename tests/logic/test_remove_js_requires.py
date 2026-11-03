import pytest
from simplibs.exception import ValidationError
from simplibs.extractor_javascript.logic import remove_js_requires

SAMPLES = [
    'const fs = require("fs")\nrun()\n',
    "const { a, b } = require('m');\nrun()\n",
    'const a = require("a")\nconst b = require("b")\nrun(a, b)\n',
    'var get = require("m").get\nrun()\n',
    'const s = `\nconst a = require("a")\n`;\n',
    "",
]


@pytest.mark.parametrize(
    "text, expected",
    [
        ('const fs = require("fs")\nrun()\n', "run()\n"),
        ("const fs = require('fs');\nrun()\n", "run()\n"),
        ('let fs = require("fs")\nrun()\n', "run()\n"),
        ('var fs = require("fs")\nrun()\n', "run()\n"),
        ('const { a, b } = require("m")\nrun()\n', "run()\n"),
        ('const { a, b: { c } } = require("m")\nrun()\n', "run()\n"),
        ('const [x, y] = require("m")\nrun()\n', "run()\n"),
        ('var get = require("m").get\nrun()\n', "run()\n"),
        ('x = 1\nconst a = require("a")\ny = 2\n', "x = 1\ny = 2\n"),
        ('run()\nconst a = require("a")', "run()"),
        ('const a = require("a")\n;\nrun()\n', "run()\n"),
        ('const a = require("a")\nconst b = require("b")\n', ""),
        ('  const a = require("a")\nrun()\n', "run()\n"),
        ('const a = require("a");\n.call()\n', ".call()\n"),
    ],
    ids=[
        "const", "single-quotes-semicolon", "let", "var", "destructuring", "nested-destructuring", "array", "member",
        "between-code", "last-without-newline", "semicolon-on-next-line", "only-requires", "indented", "semicolon-ends-it",
    ],
)
def test_the_require_goes_with_its_line(text, expected) -> None:
    assert remove_js_requires(text) == expected


def test_a_text_without_requires_stays_as_it_is() -> None:
    text = "function f(a,b){\n  return  a+b\n}\n"
    assert remove_js_requires(text) == text


def test_an_empty_text_stays_empty() -> None:
    assert remove_js_requires("") == ""


def test_all_requires_of_a_file_go_and_the_code_stays() -> None:
    text = (
        'const fs = require("fs");\n'
        'const { join } = require("path");\n'
        "\n"
        "function read(name) {\n"
        "  return fs.readFileSync(join(__dirname, name));\n"
        "}\n"
        "module.exports = { read };\n"
    )
    assert remove_js_requires(text) == (
        "\n"
        "function read(name) {\n"
        "  return fs.readFileSync(join(__dirname, name));\n"
        "}\n"
        "module.exports = { read };\n"
    )


# ---------------------------------------------------------------- what stays

@pytest.mark.parametrize(
    "text",
    [
        'const a = require("a"), b = require("b")\n',
        "const x = require(name)\n",
        'const x = require("a" + b)\n',
        'const x = require("m")()\n',
        'const x = require("m").a.b\n',
        'const x = await require("m")\n',
        'x = require("m")\n',
        'module.exports = require("m")\n',
        'export const x = require("m")\n',
        'const { a = 1 } = require("m")\n',
        'const x = require("m") // note\n',
        'const x = import("m")\n',
        'const s = "const a = require(\'a\')"\n',
    ],
    ids=[
        "two-declarators", "variable", "expression", "called", "two-members", "await", "no-declaration", "assignment",
        "exported", "default-value", "comment-after", "dynamic-import", "string",
    ],
)
def test_code_that_is_not_a_plain_dependency_stays(text) -> None:
    assert remove_js_requires(text) == text


@pytest.mark.parametrize("continuation", [", b = require('b')", ".call()", "(1)", "+ 1", "? a : b"])
def test_a_declaration_that_the_next_line_goes_on_with_stays(continuation) -> None:
    """Removing the first line would leave a broken second one."""
    text = f'var a = require("a")\n{continuation}\n'
    assert remove_js_requires(text) == text


def test_a_line_inside_a_block_comment_stays() -> None:
    text = '/*\nconst a = require("a")\n*/\nrun()\n'
    assert remove_js_requires(text) == text


def test_a_line_inside_a_template_literal_stays() -> None:
    text = 'const sample = `\nconst a = require("a")\n`;\n'
    assert remove_js_requires(text) == text


def test_a_real_require_next_to_one_in_a_template() -> None:
    text = 'const a = require("a")\nconst s = `\nconst b = require("b")\n`;\n'
    assert remove_js_requires(text) == 'const s = `\nconst b = require("b")\n`;\n'


def test_the_es_imports_are_not_its_business() -> None:
    text = 'import a from "a"\nconst b = require("b")\n'
    assert remove_js_requires(text) == 'import a from "a"\n'


# ---------------------------------------------------------------- guarantees

@pytest.mark.parametrize("text", SAMPLES)
def test_a_second_run_changes_nothing(text) -> None:
    once = remove_js_requires(text)
    assert remove_js_requires(once) == once


@pytest.mark.parametrize("text", ["'", '"', "`", "/*", "//", "/", "${", "`${", "const a = require(", "const { = require('m')"])
def test_a_text_that_is_not_valid_javascript_never_raises(text) -> None:
    assert isinstance(remove_js_requires(text), str)


@pytest.mark.parametrize("value", [None, 5, b'const a = require("a")', ['const a = require("a")']])
def test_the_text_must_be_a_str(value) -> None:
    with pytest.raises(ValidationError):
        remove_js_requires(value)
