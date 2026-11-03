import pytest
import simplibs.extractor_javascript as extractor_javascript
from pathlib import Path

EXPECTED = {
    # steps
    "js_comment_spans",
    "remove_js_imports",
    "remove_js_requires",
    "strip_js_comments",
    "strip_js_exports",
    # add-on of the extractor
    "register_all",
}

STEPS = [
    "js_comment_spans",
    "remove_js_imports",
    "remove_js_requires",
    "strip_js_comments",
    "strip_js_exports",
]

# The four domain folders are public through their own `__all__`, not through the root.
DOMAINS = {
    "actions": {
        "RemoveJsImports",
        "RemoveJsRequires",
        "StripJsComments",
        "StripJsExports",
    },
    "file_rules": {
        "DEPENDENCY_DIRS",
        "DOT_NAME",
        "INDEX_NAME",
        "OUTPUT_DIRS",
        "UNDERSCORE_NAME",
        "VCS_DIRS",
        "JS_ASSET_DIRS",
        "JS_BASE",
        "JS_CONFIG",
        "JS_FILES",
        "JS_STRICT_EXCLUDE",
        "JS_TESTS",
        "build_js_base",
    },
    "presets": {
        "JS_CLEAN",
        "JS_NO_IMPORTS",
    },
    "profiles": {
        "JS_CODE_CLEAN",
        "JS_CODE_NO_IMPORTS",
        "JS_DATA_ALL",
        "JS_PROFILES",
        "JS_SRC_CLEAN",
    },
}

SUBPACKAGES = {"constants", "file_rules", "logic", "actions", "presets", "profiles", "plugin"}


def test_the_public_names_are_exactly_the_agreed_ones() -> None:
    """Adding or removing a public name is a decision; it must change this test on purpose."""
    assert set(extractor_javascript.__all__) == EXPECTED
    assert len(extractor_javascript.__all__) == 6


def test_no_name_is_listed_twice() -> None:
    assert len(extractor_javascript.__all__) == len(set(extractor_javascript.__all__))


@pytest.mark.parametrize("name", sorted(EXPECTED))
def test_every_public_name_exists(name) -> None:
    assert hasattr(extractor_javascript, name)


def test_a_star_import_brings_exactly_the_public_names() -> None:
    namespace: dict = {}
    exec("from simplibs.extractor_javascript import *", namespace)
    namespace.pop("__builtins__")
    assert set(namespace) == EXPECTED


def test_nothing_else_is_public() -> None:
    """Besides the public names, the package shows only its own sub-packages."""
    public = {name for name in dir(extractor_javascript) if not name.startswith("_")}
    assert public - set(extractor_javascript.__all__) <= SUBPACKAGES


@pytest.mark.parametrize("name", [*STEPS, "register_all"])
def test_the_steps_and_the_entry_point_are_callable(name) -> None:
    assert callable(getattr(extractor_javascript, name)), name


def test_the_steps_are_the_ones_of_the_logic_layer() -> None:
    import simplibs.extractor_javascript.logic as logic

    for name in STEPS:
        assert getattr(extractor_javascript, name) is getattr(logic, name), name


# ---------------------------------------------------------------- the domain folders

@pytest.mark.parametrize("domain", sorted(DOMAINS))
def test_the_domain_has_exactly_the_agreed_names(domain) -> None:
    import importlib

    module = importlib.import_module(f"simplibs.extractor_javascript.{domain}")
    assert set(module.__all__) == DOMAINS[domain]
    assert len(module.__all__) == len(set(module.__all__)), "a name is listed twice"


@pytest.mark.parametrize("domain", sorted(DOMAINS))
def test_every_name_of_a_domain_exists(domain) -> None:
    import importlib

    module = importlib.import_module(f"simplibs.extractor_javascript.{domain}")
    for name in DOMAINS[domain]:
        assert hasattr(module, name), name


def test_the_root_does_not_re_export_the_domains() -> None:
    domain_names = set().union(*DOMAINS.values())
    assert domain_names & set(extractor_javascript.__all__) == set()


def test_the_domains_do_not_share_a_name_with_each_other_by_accident() -> None:
    """`DOT_NAME` and the like are listed once, in `file_rules`; no other domain repeats a name."""
    seen: dict[str, str] = {}
    repeated = []
    for domain, names in DOMAINS.items():
        for name in names:
            if name in seen:
                repeated.append(f"{name}: {seen[name]}, {domain}")
            seen[name] = domain
    assert repeated == []


# ---------------------------------------------------------------- the package as a whole

def test_the_package_is_marked_as_typed() -> None:
    assert (Path(extractor_javascript.__file__).parent / "py.typed").is_file()
