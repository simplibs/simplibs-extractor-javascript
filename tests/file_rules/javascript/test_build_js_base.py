from pathlib import Path
import pytest
from simplibs.exception import ValidationError
from simplibs.rules import Rule
from simplibs.rules.testing import assert_rule_contract
from simplibs.extractor_javascript.file_rules import build_js_base

ALWAYS_TAKEN = [
    "a.js",
    "src/App.tsx",
    "src/c.jsx",
    "src/d.ts",
    "src/a.mjs",
    "src/b.cjs",
    "pkg/a.min.js",
    "types.d.ts",
    "src/a.test.js",
    "node_modules/x/a.js",
    "src/_private/a.js",
]
ALWAYS_LEFT_OUT = [
    "a.json",
    "a.css",
    "README.md",
    "a.py",
    "package.json",
    ".hidden.js",
    "src/.eslintrc.js",
    ".index.js",
    "._app.js",
]
INDEX = ["index.js", "src/index.tsx", "components/Button/index.ts"]
UNDERSCORE = ["_app.tsx", "pages/_document.tsx", "_helpers.js"]


def _paths(*groups) -> list[Path]:
    return [Path(path) for group in groups for path in group]


def test_returns_a_rule() -> None:
    assert isinstance(build_js_base(), Rule)


@pytest.mark.parametrize(
    "include_index, include_underscore",
    [(True, True), (True, False), (False, True), (False, False)],
    ids=["both", "index-only", "underscore-only", "neither"],
)
def test_rule_contract(subtests, include_index, include_underscore) -> None:
    taken = [*ALWAYS_TAKEN, *(INDEX if include_index else []), *(UNDERSCORE if include_underscore else [])]
    left_out = [*ALWAYS_LEFT_OUT, *([] if include_index else INDEX), *([] if include_underscore else UNDERSCORE)]
    assert_rule_contract(
        subtests,
        build_js_base(include_index=include_index, include_underscore=include_underscore),
        valid_values=_paths(taken),
        invalid_values=_paths(left_out),
        check_slots=False,
        check_value=False,
        verbose=False,
    )


def test_the_defaults_take_the_entry_and_the_framework_files() -> None:
    """The old rule dropped every `index.*` and every `_*`: the root `index.js` and `pages/_app.tsx` were lost."""
    rule = build_js_base()
    assert all(rule(path) is True for path in _paths(INDEX, UNDERSCORE))


def test_switching_the_index_off_leaves_the_underscore_files() -> None:
    rule = build_js_base(include_index=False)
    assert rule(Path("src/index.tsx")) is False
    assert rule(Path("pages/_app.tsx")) is True


def test_switching_the_underscore_off_leaves_the_index_files() -> None:
    rule = build_js_base(include_underscore=False)
    assert rule(Path("pages/_app.tsx")) is False
    assert rule(Path("src/index.tsx")) is True


def test_both_off_brings_back_the_old_behaviour() -> None:
    rule = build_js_base(include_index=False, include_underscore=False)
    assert rule(Path("src/index.tsx")) is False
    assert rule(Path("pages/_app.tsx")) is False
    assert rule(Path("src/App.tsx")) is True


def test_a_dot_file_is_left_out_whatever_the_switches_say() -> None:
    rule = build_js_base(include_index=True, include_underscore=True)
    assert rule(Path(".eslintrc.js")) is False


def test_every_call_builds_its_own_rule() -> None:
    assert build_js_base() is not build_js_base()


@pytest.mark.parametrize("option", ["include_index", "include_underscore"])
@pytest.mark.parametrize("value", ["yes", None, [True]])
def test_the_switches_must_be_bool(option, value) -> None:
    with pytest.raises(ValidationError):
        build_js_base(**{option: value})


def test_the_switches_are_keyword_only() -> None:
    with pytest.raises(TypeError):
        build_js_base(True)  # type: ignore[misc]
