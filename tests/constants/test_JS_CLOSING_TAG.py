import re
import pytest
from simplibs.extractor_javascript.constants import JS_CLOSING_TAG


def test_is_a_compiled_pattern() -> None:
    assert isinstance(JS_CLOSING_TAG, re.Pattern)


@pytest.mark.parametrize(
    "text",
    ["/div>", "/Foo.Bar >", "/>", "/svg:rect>", "/my-comp>", "/$x>", "/div >", "/a.b.c>", "/h1>"],
    ids=["tag", "dotted-with-space", "fragment", "namespace", "dashed", "dollar", "space-before-end", "deep-dotted", "digit"],
)
def test_the_slash_of_a_closing_tag_is_matched(text) -> None:
    assert JS_CLOSING_TAG.match(text) is not None


@pytest.mark.parametrize(
    "text",
    ["/image\\/x/.test(s)", "/ab/", "/=/", "/* c */", "// c", "/div", "/div(>", "/ a>", "/a b>", "/[a-z]>/.test(x)"],
    ids=["regex-with-escape", "regex", "regex-equals", "block-comment", "line-comment", "unfinished", "paren", "space-then-name", "two-words", "class"],
)
def test_the_slash_of_a_regular_expression_is_not(text) -> None:
    assert JS_CLOSING_TAG.match(text) is None


def test_it_is_tried_at_the_slash_not_in_the_middle_of_a_text() -> None:
    assert JS_CLOSING_TAG.match("n </div>") is None
    assert JS_CLOSING_TAG.match("n </div>", 3) is not None


def test_the_match_ends_with_the_closing_bracket() -> None:
    assert JS_CLOSING_TAG.match("/div> text").group(0) == "/div>"
