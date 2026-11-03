from simplibs.extractor_javascript.constants import JS_OUTPUT_DIR_NAMES


def test_value() -> None:
    assert JS_OUTPUT_DIR_NAMES == ("build", "dist", "out", ".next")


def test_is_a_tuple_of_strings() -> None:
    assert isinstance(JS_OUTPUT_DIR_NAMES, tuple)
    assert all(isinstance(name, str) for name in JS_OUTPUT_DIR_NAMES)


def test_no_name_is_listed_twice() -> None:
    assert len(JS_OUTPUT_DIR_NAMES) == len(set(JS_OUTPUT_DIR_NAMES))


def test_every_name_is_a_single_folder_name() -> None:
    for name in JS_OUTPUT_DIR_NAMES:
        assert name and name == name.strip(), name
        assert "/" not in name and "\\" not in name, name
        assert not any(char.isspace() for char in name), name


def test_the_build_folder_of_next_js_is_named_although_it_starts_with_a_dot() -> None:
    """The base rule leaves out dot FILES only; without this name the compiled pages would be read as source."""
    assert ".next" in JS_OUTPUT_DIR_NAMES
