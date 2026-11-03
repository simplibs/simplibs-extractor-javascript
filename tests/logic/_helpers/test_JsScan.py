import dataclasses
import pytest
from simplibs.extractor_javascript.logic._helpers import JsScan


def test_holds_the_three_lists() -> None:
    scan = JsScan(((0, 1),), ((0, 1),), ((2, 3),))
    assert scan.comments == ((0, 1),)
    assert scan.glued == ((0, 1),)
    assert scan.literals == ((2, 3),)


def test_is_frozen() -> None:
    scan = JsScan((), (), ())
    with pytest.raises(dataclasses.FrozenInstanceError):
        scan.comments = ((0, 1),)  # type: ignore[misc]


def test_has_no_instance_dict() -> None:
    assert not hasattr(JsScan((), (), ()), "__dict__")


def test_two_scans_with_the_same_content_are_equal() -> None:
    assert JsScan(((0, 1),), (), ()) == JsScan(((0, 1),), (), ())
    assert JsScan(((0, 1),), (), ()) != JsScan((), (), ())


def test_the_order_of_the_fields() -> None:
    assert [field.name for field in dataclasses.fields(JsScan)] == ["comments", "glued", "literals"]
