import importlib.metadata
from types import SimpleNamespace
import pytest
from simplibs.extractor import get_profile, load_plugins
from simplibs.extractor.constants import PLUGIN_GROUP
from simplibs.extractor.registry._helpers import PROFILE_REGISTRY
from simplibs.extractor_javascript import register_all
from simplibs.extractor_javascript.profiles import JS_PROFILES

KEYS = [profile.key for profile in JS_PROFILES]


@pytest.fixture(autouse=True)
def without_the_javascript_profiles():
    for key in KEYS:
        PROFILE_REGISTRY.pop(key, None)


def _finder(*entry_points):
    return lambda *, group: list(entry_points) if group == PLUGIN_GROUP else []


def test_the_extractor_loads_the_add_on_the_way_an_installed_one_is_loaded() -> None:
    entry_point = SimpleNamespace(name="javascript", load=lambda: register_all)
    loaded, failed = load_plugins(entry_points=_finder(entry_point))
    assert loaded == ["javascript"]
    assert failed == {}


def test_after_loading_every_profile_of_the_add_on_is_in_the_registry() -> None:
    entry_point = SimpleNamespace(name="javascript", load=lambda: register_all)
    load_plugins(entry_points=_finder(entry_point))
    for profile in JS_PROFILES:
        assert get_profile(profile.key) is profile


def test_loading_twice_is_safe() -> None:
    entry_point = SimpleNamespace(name="javascript", load=lambda: register_all)
    first = load_plugins(entry_points=_finder(entry_point))
    second = load_plugins(entry_points=_finder(entry_point))
    assert first == second == (["javascript"], {})


def test_the_add_on_is_called_with_no_arguments() -> None:
    """The extractor calls `entry_point.load()()`, so the function must need nothing."""
    calls = []

    def load():
        def call():
            calls.append(register_all())
        return call

    load_plugins(entry_points=_finder(SimpleNamespace(name="javascript", load=load)))
    assert calls == [KEYS]


def test_the_entry_point_of_the_installed_package_points_to_register_all() -> None:
    """Only when the library is installed (`pip install -e .`); otherwise the test is skipped."""
    found = {entry_point.name: entry_point for entry_point in importlib.metadata.entry_points(group=PLUGIN_GROUP)}
    if "javascript" not in found:
        pytest.skip("simplibs-extractor-javascript is not installed: run `pip install -e .`")
    assert found["javascript"].load() is register_all


def test_the_python_add_on_and_this_one_load_together_without_a_clash() -> None:
    """Only when both are installed in this environment; otherwise the test is skipped."""
    python_addon = pytest.importorskip("simplibs.extractor_python")
    entries = [
        SimpleNamespace(name="python", load=lambda: python_addon.register_all),
        SimpleNamespace(name="javascript", load=lambda: register_all),
    ]
    loaded, failed = load_plugins(entry_points=_finder(*entries))
    assert loaded == ["python", "javascript"]
    assert failed == {}
    assert all(get_profile(key) for key in KEYS)
    assert len({profile.key for profile in python_addon.profiles.PYTHON_PROFILES} & set(KEYS)) == 0
