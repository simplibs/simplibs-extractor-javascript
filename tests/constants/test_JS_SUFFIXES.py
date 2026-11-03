from simplibs.extractor.definitions._helpers import is_suffix_key
from simplibs.extractor_javascript.constants import JS_SUFFIXES


def test_value() -> None:
    assert JS_SUFFIXES == (".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs")


def test_is_a_tuple_of_strings() -> None:
    assert isinstance(JS_SUFFIXES, tuple)
    assert all(isinstance(suffix, str) for suffix in JS_SUFFIXES)


def test_no_suffix_is_listed_twice() -> None:
    assert len(JS_SUFFIXES) == len(set(JS_SUFFIXES))


def test_the_module_suffixes_the_old_code_did_not_know_are_there() -> None:
    assert ".mjs" in JS_SUFFIXES
    assert ".cjs" in JS_SUFFIXES


def test_javascript_typescript_and_react_are_all_covered() -> None:
    for suffix in (".js", ".jsx", ".ts", ".tsx"):
        assert suffix in JS_SUFFIXES


def test_every_suffix_is_a_valid_key_of_a_steps_mapping() -> None:
    """The profiles use the suffixes as keys of `by_suffix`, so each one must be a lowercase suffix with a dot."""
    for suffix in JS_SUFFIXES:
        assert is_suffix_key(suffix), suffix
        assert suffix != "*", suffix
