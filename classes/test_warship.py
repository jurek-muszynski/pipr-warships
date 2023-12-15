from warship import Warship
from warship import InvalidCoordinatesError
import pytest


def test_create_warship_standard():
    blocks = [
        (0, 0), (0, 1), (0, 2)
    ]
    warship = Warship(blocks, 3)
    assert warship.size == 3
    assert warship.blocks == blocks
    assert warship.hits == 0


def test_create_warship_invalid():
    with pytest.raises(ValueError):
        Warship([("A", "0")], 1)
    with pytest.raises(InvalidCoordinatesError):
        Warship([("1", "0")], 1)
    with pytest.raises(InvalidCoordinatesError):
        Warship([("0", "2")], 1)


def test_warship_str_std():
    blocks = [
        (0, 0), (0, 1), (0, 2)
    ]
    warship = Warship(blocks, 3)
    assert str(warship) == "3 mast warship"


def test_warship_hit_std():
    blocks = [
        (0, 0), (0, 1), (0, 2)
    ]
    warship = Warship(blocks, 3)
    assert warship.hits == 0
    warship.was_hit((1, 0))
    assert warship.hits == 0
    warship.was_hit((0, 0))
    assert warship.hits == 1


def test_warship_hit_sunk():
    blocks = [
        (0, 0), (0, 1), (0, 2)
    ]
    warship = Warship(blocks, 3)
    assert warship.hits == 0
    assert warship.was_sunk() is not True
    warship.was_hit((0, 0))
    warship.was_hit((0, 1))
    warship.was_hit((0, 2))
    assert warship.hits == 3
    assert warship.was_sunk() is True
