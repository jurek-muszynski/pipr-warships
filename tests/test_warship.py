from warship import Warship
import pytest


def test_create_warship_standard():
    """
    Test warships's constructor method\n
    This test targets the standard use case
    """
    blocks = [
        (0, 0), (0, 1), (0, 2)
    ]
    warship = Warship(blocks)
    assert warship.evaluate_blocks(blocks)
    assert warship.size == 3
    assert warship.blocks == blocks
    assert warship.hits == 0


def test_create_warship_invalid():
    """
    Test warships's constructor method\n
    This test targets incorrect use cases
    """
    blocks = []
    with pytest.raises(ValueError):
        Warship(blocks)
    blocks = [(0, 0), (0, 2), (0, 3)]
    with pytest.raises(ValueError):
        Warship(blocks)
    blocks = [(-1, 0), (0, 0), (1, 0)]
    with pytest.raises(ValueError):
        Warship(blocks)


def test_warship_str_std():
    """
    Test warships's __str__() method\n
    This test targets the standard use case
    """
    blocks = [
        (0, 0), (0, 1), (0, 2)
    ]
    warship = Warship(blocks)
    assert str(warship) == "3 mast warship"


def test_warship_hit_std():
    """
    Test warships's hit() method\n
    This test targets the standard use case
    """
    blocks = [
        (0, 0), (0, 1), (0, 2)
    ]
    warship = Warship(blocks)
    assert warship.hits == 0
    assert not warship.was_hit((1, 0))
    assert warship.hits == 0
    assert warship.was_hit((0, 0))
    assert warship.hits == 1


def test_warship_hit_same_block():
    """
    Test warships's hit() method\n
    This test targets the case, when a hit
    was repeated
    """
    blocks = [
        (0, 0), (0, 1), (0, 2)
    ]
    warship = Warship(blocks)
    assert warship.hits == 0
    assert warship.was_hit((0, 0))
    assert warship.hits == 1
    assert not warship.was_hit((0, 0))
    assert warship.hits == 1


def test_warship_hit_sink():
    """
    Test warships's hit() method\n
    This test targets the case when
    a warship was sunk
    """
    blocks = [
        (0, 0), (0, 1), (0, 2)
    ]
    warship = Warship(blocks)
    assert warship.hits == 0
    assert warship.was_sunk() is not True
    assert warship.was_hit((0, 0))
    assert warship.was_hit((0, 1))
    assert not warship.was_hit((0, 3))
    assert warship.was_hit((0, 2))
    assert warship.hits == 3
    assert warship.was_sunk() is True
