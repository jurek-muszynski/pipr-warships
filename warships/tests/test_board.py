from board import Board
from board import InvalidWarshipCountError, InvalidWarshipError
from warship import Warship
import pytest


def test_create_board_std():
    board = Board(4, 4)
    assert board.size == 4
    assert board.num_warships == 4
    assert not board.warships()


def test_create_board_invalid():
    with pytest.raises(ValueError):
        Board(0, 1)
    with pytest.raises(ValueError):
        Board(1, 0)
    with pytest.raises(ValueError):
        Board(-10, 5)
    with pytest.raises(ValueError):
        Board(1, -1)
    with pytest.raises(InvalidWarshipCountError):
        Board(4, 5)


def test_add_warship_std():
    board = Board(4, 4)
    blocks = [(0, 0), (0, 1), (0, 2), (0, 3)]
    board.add_warship(blocks)
    assert board.warships() == "4 mast warship "


def test_add_warship_invalid():
    board = Board(4, 4)
    blocks = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]
    with pytest.raises(InvalidWarshipError):
        board.add_warship(blocks)
    with pytest.raises(InvalidWarshipError):
        board.add_warship([(0, 4)])
