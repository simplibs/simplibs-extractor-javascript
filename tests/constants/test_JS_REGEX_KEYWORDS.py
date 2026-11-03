from simplibs.extractor_javascript.constants import JS_REGEX_KEYWORDS


def test_value() -> None:
    assert JS_REGEX_KEYWORDS == frozenset({
        "return", "typeof", "case", "do", "else", "in", "of", "void",
        "delete", "throw", "new", "yield", "await", "instanceof",
    })


def test_is_a_frozenset_of_strings() -> None:
    assert isinstance(JS_REGEX_KEYWORDS, frozenset)
    assert all(isinstance(word, str) for word in JS_REGEX_KEYWORDS)


def test_every_word_is_a_lowercase_word() -> None:
    for word in JS_REGEX_KEYWORDS:
        assert word.isidentifier() and word == word.lower(), word


def test_a_word_that_ends_an_expression_is_not_listed() -> None:
    """After `this`, `null` or `true` a slash divides: they are values, not the start of an expression."""
    for word in ("this", "null", "true", "false", "undefined", "super"):
        assert word not in JS_REGEX_KEYWORDS, word
