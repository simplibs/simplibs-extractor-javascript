from simplibs.extractor_javascript.constants import JS_SEPARATORS


def test_value() -> None:
    assert JS_SEPARATORS == " \t\r\n{}()[],;"


def test_is_a_str() -> None:
    assert isinstance(JS_SEPARATORS, str)


def test_no_character_is_listed_twice() -> None:
    assert len(JS_SEPARATORS) == len(set(JS_SEPARATORS))


def test_every_kind_of_whitespace_that_ends_a_token_is_there() -> None:
    for character in (" ", "\t", "\r", "\n"):
        assert character in JS_SEPARATORS


def test_the_brackets_commas_and_semicolons_are_there() -> None:
    for character in "{}()[],;":
        assert character in JS_SEPARATORS


def test_nothing_that_can_be_part_of_a_token_or_glue_two_of_them_is_there() -> None:
    """`a+/**/+b` must not become `a++b`, and `a/**/b` must not become `ab`: only real separators may be listed."""
    for character in JS_SEPARATORS:
        assert not character.isalnum(), character
        assert character not in "$_.+-*/<>=!&|^~?:\"'`#@\\", character
