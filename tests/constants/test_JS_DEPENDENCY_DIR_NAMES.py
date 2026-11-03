from simplibs.extractor_javascript.constants import JS_DEPENDENCY_DIR_NAMES


def test_value() -> None:
    assert JS_DEPENDENCY_DIR_NAMES == ("node_modules",)


def test_is_a_tuple_of_strings() -> None:
    assert isinstance(JS_DEPENDENCY_DIR_NAMES, tuple)
    assert all(isinstance(name, str) for name in JS_DEPENDENCY_DIR_NAMES)


def test_every_name_is_a_single_folder_name() -> None:
    for name in JS_DEPENDENCY_DIR_NAMES:
        assert name and name == name.strip(), name
        assert "/" not in name and "\\" not in name, name
