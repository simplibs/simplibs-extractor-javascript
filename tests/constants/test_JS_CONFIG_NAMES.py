from simplibs.extractor_javascript.constants import JS_CONFIG_NAMES


def test_value() -> None:
    assert JS_CONFIG_NAMES == (
        "package.json",
        "package-lock.json",
        "yarn.lock",
        "pnpm-lock.yaml",
        "tsconfig.json",
        "next.config.js",
        "next.config.ts",
        "tailwind.config.js",
        "tailwind.config.ts",
        "postcss.config.js",
        "vite.config.ts",
        "webpack.config.js",
        "babel.config.js",
        "jest.config.js",
        "jest.config.ts",
        ".eslintrc.js",
        ".prettierrc",
    )


def test_is_a_tuple_of_strings() -> None:
    assert isinstance(JS_CONFIG_NAMES, tuple)
    assert all(isinstance(name, str) for name in JS_CONFIG_NAMES)


def test_no_name_is_listed_twice() -> None:
    assert len(JS_CONFIG_NAMES) == len(set(JS_CONFIG_NAMES))


def test_every_name_is_a_plain_file_name() -> None:
    """A name is compared with the name of a file, so it holds no folder and no whitespace."""
    for name in JS_CONFIG_NAMES:
        assert name and name == name.strip(), name
        assert "/" not in name and "\\" not in name, name
        assert not any(char.isspace() for char in name), name


def test_the_dot_files_are_named_too() -> None:
    """The base rule already leaves dot files out; the names are here so a wider own `include` is covered."""
    assert ".eslintrc.js" in JS_CONFIG_NAMES
    assert ".prettierrc" in JS_CONFIG_NAMES
