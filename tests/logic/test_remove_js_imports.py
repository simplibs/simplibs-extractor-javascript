import pytest
from simplibs.exception import ValidationError
from simplibs.extractor_javascript.logic import remove_js_imports, strip_js_comments

SAMPLES = [
    'import a from "a"\nconst x = 1\n',
    "import a from 'a';\nimport { b } from 'b';\n\nconst x = a + b\n",
    'import {\n  a,\n  b as c,\n} from "m";\nrun(a, c)\n',
    'import type { T } from "m"\nlet x: T\n',
    'import "side-effect"\nrun()\n',
    'import * as ns from "m"\nimport def, { x } from "n"\nrun()\n',
    'const lazy = () => import("./lazy")\n',
    'const s = `\nimport a from "a"\n`;\n',
    "",
]


@pytest.mark.parametrize(
    "text, expected",
    [
        ('import a from "a"\nconst x = 1\n', "const x = 1\n"),
        ("import a from 'a';\nconst x = 1\n", "const x = 1\n"),
        ('import { a, b as c } from "m"\nrun()\n', "run()\n"),
        ('import * as ns from "m"\nrun()\n', "run()\n"),
        ('import def, { a } from "m"\nrun()\n', "run()\n"),
        ('import "side-effect"\nrun()\n', "run()\n"),
        ('import type { T } from "m"\nlet x: T\n', "let x: T\n"),
        ('import {\n  a,\n  b,\n} from "m";\nrun()\n', "run()\n"),
        ('x = 1\nimport a from "a"\ny = 2\n', "x = 1\ny = 2\n"),
        ('run()\nimport a from "a"', "run()"),
        ('import a from "a"\n;\nrun()\n', "run()\n"),
        ('import a from "a"\nimport b from "b"\n', ""),
        ("  import a from 'a'\nrun()\n", "run()\n"),
    ],
    ids=[
        "default", "single-quotes", "named", "namespace", "default-and-named", "side-effect", "type", "several-lines",
        "between-code", "last-without-newline", "semicolon-on-next-line", "only-imports", "indented",
    ],
)
def test_the_import_goes_with_its_line(text, expected) -> None:
    assert remove_js_imports(text) == expected


def test_a_text_without_imports_stays_as_it_is() -> None:
    text = "function f(a,b){\n  return  a+b\n}\n"
    assert remove_js_imports(text) == text


def test_an_empty_text_stays_empty() -> None:
    assert remove_js_imports("") == ""


def test_all_imports_of_a_file_go_and_the_code_stays() -> None:
    text = (
        'import React from "react";\n'
        'import { useState } from "react";\n'
        'import type { Props } from "./types";\n'
        "\n"
        "export function App(props: Props) {\n"
        "  const [n, setN] = useState(0);\n"
        "  return n;\n"
        "}\n"
    )
    assert remove_js_imports(text) == (
        "\n"
        "export function App(props: Props) {\n"
        "  const [n, setN] = useState(0);\n"
        "  return n;\n"
        "}\n"
    )


# ---------------------------------------------------------------- what stays

@pytest.mark.parametrize(
    "text",
    [
        'const lazy = () => import("./lazy")\n',
        'import("m").then(f)\n',
        'import ("m")\n',
        'const m = await import("m")\n',
        'import.meta.url\n',
        'import a from "a"; run()\n',
        'import a from "a" // note\n',
        'import a from "a" /* note */\n',
        'export { a } from "m"\n',
        'const s = "import a from \'a\'"\n',
        'important = 1\n',
    ],
    ids=[
        "lazy", "dynamic", "dynamic-with-space", "await", "meta", "code-after", "comment-after", "block-comment-after",
        "re-export", "string", "other-word",
    ],
)
def test_an_expression_and_a_statement_that_shares_its_line_stay(text) -> None:
    assert remove_js_imports(text) == text


def test_a_line_inside_a_block_comment_stays() -> None:
    text = '/*\nimport a from "a"\n*/\nrun()\n'
    assert remove_js_imports(text) == text


def test_a_line_inside_a_template_literal_stays() -> None:
    text = 'const sample = `\nimport a from "a"\n`;\n'
    assert remove_js_imports(text) == text


def test_an_indented_line_inside_a_template_literal_stays() -> None:
    text = 'const sample = `\n    import a from "a"\n`;\n'
    assert remove_js_imports(text) == text


def test_a_real_import_next_to_one_in_a_template() -> None:
    text = 'import a from "a"\nconst s = `\nimport b from "b"\n`;\n'
    assert remove_js_imports(text) == 'const s = `\nimport b from "b"\n`;\n'


# ---------------------------------------------------------------- order and guarantees

def test_an_import_followed_by_a_comment_goes_once_the_comments_are_gone() -> None:
    text = 'import a from "a" // the a\nrun(a)\n'
    assert remove_js_imports(text) == text
    assert remove_js_imports(strip_js_comments(text)) == "run(a)\n"


@pytest.mark.parametrize("text", ['import a from "a"\n// note\nrun(a) // c\n', '/* head */\nimport a from "a"\nrun(a)\n'])
def test_the_order_of_the_comment_step_does_not_matter_for_a_plain_import(text) -> None:
    assert remove_js_imports(strip_js_comments(text)) == strip_js_comments(remove_js_imports(text))


@pytest.mark.parametrize("text", SAMPLES)
def test_a_second_run_changes_nothing(text) -> None:
    once = remove_js_imports(text)
    assert remove_js_imports(once) == once


@pytest.mark.parametrize("text", ["'", '"', "`", "/*", "//", "/", "${", "`${", "import", "import '", "x = (\nimport a from 'b'"])
def test_a_text_that_is_not_valid_javascript_never_raises(text) -> None:
    assert isinstance(remove_js_imports(text), str)


# ---------------------------------------------------------------- the arguments

@pytest.mark.parametrize("value", [None, 5, b'import a from "a"', ['import a from "a"']])
def test_the_text_must_be_a_str(value) -> None:
    with pytest.raises(ValidationError):
        remove_js_imports(value)
