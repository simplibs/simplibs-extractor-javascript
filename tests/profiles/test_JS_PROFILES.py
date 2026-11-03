from simplibs.extractor import Profile
from simplibs.extractor_javascript.profiles import (
    JS_CODE_CLEAN,
    JS_CODE_NO_IMPORTS,
    JS_DATA_ALL,
    JS_PROFILES,
    JS_SRC_CLEAN,
)


def test_is_a_tuple_of_profiles() -> None:
    assert isinstance(JS_PROFILES, tuple)
    assert all(isinstance(profile, Profile) for profile in JS_PROFILES)


def test_holds_the_four_profiles_in_the_order_of_the_listing() -> None:
    assert JS_PROFILES == (JS_CODE_CLEAN, JS_CODE_NO_IMPORTS, JS_DATA_ALL, JS_SRC_CLEAN)


def test_the_keys_in_the_order_of_the_listing() -> None:
    assert [profile.key for profile in JS_PROFILES] == [
        "javascript/code-clean",
        "javascript/code-no-imports",
        "javascript/data-all",
        "javascript/src-clean",
    ]


def test_every_profile_belongs_to_the_system_javascript() -> None:
    assert {profile.system for profile in JS_PROFILES} == {"javascript"}


def test_the_keys_are_unique() -> None:
    keys = [profile.key for profile in JS_PROFILES]
    assert len(keys) == len(set(keys))


def test_the_output_names_are_unique() -> None:
    """Two profiles that wrote the same file would overwrite each other's output."""
    names = [profile.output_name for profile in JS_PROFILES]
    assert len(names) == len(set(names))


def test_the_output_names_start_with_the_system() -> None:
    assert all(profile.output_name.startswith("javascript_") for profile in JS_PROFILES)


def test_every_profile_has_a_description() -> None:
    assert all(profile.description.strip() for profile in JS_PROFILES)


def test_the_profiles_are_in_the_listing_order_of_their_keys() -> None:
    keys = [profile.key for profile in JS_PROFILES]
    assert keys == sorted(keys)


def test_all_the_profiles_take_the_same_files_before_any_exclusion() -> None:
    from simplibs.extractor_javascript.file_rules import JS_BASE

    assert all(profile.include is JS_BASE for profile in JS_PROFILES)
