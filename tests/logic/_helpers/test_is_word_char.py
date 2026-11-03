import pytest
from simplibs.extractor_javascript.logic._helpers import is_word_char


@pytest.mark.parametrize("character", ["a", "Z", "m", "0", "9", "_", "$", "é", "ž", "ß", "中", "ж", "٣"])
def test_a_letter_a_digit_an_underscore_and_a_dollar_belong_to_a_name(character) -> None:
    assert is_word_char(character) is True


@pytest.mark.parametrize("character", [" ", "\t", "\n", "\r", "-", ".", "/", "'", '"', "`", "(", ")", "{", "}", "#", "@", "\\", "+", "*", ",", ";", ":", "<", ">", "="])
def test_everything_else_does_not(character) -> None:
    assert is_word_char(character) is False


def test_returns_a_real_bool() -> None:
    assert type(is_word_char("a")) is bool
    assert type(is_word_char(" ")) is bool
