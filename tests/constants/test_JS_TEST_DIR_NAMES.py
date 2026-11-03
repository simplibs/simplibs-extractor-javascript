from simplibs.extractor_javascript.constants import JS_TEST_DIR_NAMES


def test_value() -> None:
    assert JS_TEST_DIR_NAMES == ("__tests__", "__mocks__", "e2e", "tests", "test", "coverage")


def test_is_a_tuple_of_strings() -> None:
    assert isinstance(JS_TEST_DIR_NAMES, tuple)
    assert all(isinstance(name, str) for name in JS_TEST_DIR_NAMES)


def test_no_name_is_listed_twice() -> None:
    assert len(JS_TEST_DIR_NAMES) == len(set(JS_TEST_DIR_NAMES))


def test_every_name_is_a_whole_folder_name() -> None:
    """Names are compared as a whole (`contest` is not `test`), so none holds a separator or whitespace."""
    for name in JS_TEST_DIR_NAMES:
        assert name and name == name.strip(), name
        assert "/" not in name and "\\" not in name, name
        assert not any(char.isspace() for char in name), name


def test_the_coverage_reports_are_listed_although_they_are_no_tests() -> None:
    """They are generated from the tests and have no place in a reading of the source."""
    assert "coverage" in JS_TEST_DIR_NAMES
