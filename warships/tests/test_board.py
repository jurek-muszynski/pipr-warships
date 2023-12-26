from board import Board
from board import (InvalidWarshipCountError, InvalidWarshipError,
                   CoordinatesOutOfRangeError)
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


def test_all_locations():
    board1 = Board(1, 1)
    assert board1.all_locations() == [(0, 0)]
    board2 = Board(2, 2)
    assert board2.all_locations() == [(0, 0), (0, 1), (1, 0), (1, 1)]


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


def test_is_location_available():
    board = Board(2, 2)
    assert board._is_location_available(0, 0)
    board.add_warship([(0, 0)])
    assert not board._is_location_available(0, 0)


def test_get_available_locations_horizontal_std():
    board = Board(2, 2)
    blocks_1 = [[(0, 0)], [(0, 1)], [(1, 0)], [(1, 1)]]
    blocks_2 = [[(0, 0), (0, 1)], [(1, 0), (1, 1)]]
    assert board.get_available_locations_horizontal(1) == blocks_1
    assert board.get_available_locations_horizontal(2) == blocks_2


def test_get_available_locations_vertical_std():
    board = Board(2, 2)
    blocks_1 = [[(0, 0)], [(0, 1)], [(1, 0)], [(1, 1)]]
    blocks_2 = [[(0, 0), (1, 0)], [(0, 1), (1, 1)]]
    assert board.get_available_locations_vertical(1) == blocks_1
    assert board.get_available_locations_vertical(2) == blocks_2


def test_get_available_locations_horizontal_added_warships():
    board = Board(2, 2)
    blocks1 = [[(1, 0)], [(1, 1)]]
    blocks2 = [[(1, 0), (1, 1)]]
    board.add_warship([(0, 0), (0, 1)])
    assert board.get_available_locations_horizontal(1) == blocks1
    assert board.get_available_locations_horizontal(2) == blocks2


def test_get_available_locations_vertical_added_warships():
    board = Board(2, 2)
    blocks1 = [[(0, 1)], [(1, 1)]]
    blocks2 = [[(0, 1), (1, 1)]]
    board.add_warship([(0, 0), (1, 0)])
    assert board.get_available_locations_vertical(1) == blocks1
    assert board.get_available_locations_vertical(2) == blocks2


def test_get_available_locations_horizontal_no_available():
    board = Board(2, 2)
    board.add_warship([(0, 0), (0, 1)])
    board.add_warship([(1, 0), (1, 1)])
    assert board.get_available_locations_horizontal(1) == []
    assert board.get_available_locations_horizontal(2) == []


def test_get_available_locations_vertical_no_available():
    board = Board(2, 2)
    board.add_warship([(0, 0), (1, 0)])
    board.add_warship([(0, 1), (1, 1)])
    assert board.get_available_locations_vertical(1) == []
    assert board.get_available_locations_vertical(2) == []


def test_draw_location_std_random():
    board = Board(2, 2)
    drawed_locations = board.draw_location(2)
    assert drawed_locations is not None
    assert len(board.get_available_locations_horizontal(1)) == 4
    assert len(board.get_available_locations_vertical(1)) == 4
    board.add_warship(drawed_locations)
    assert len(board.get_available_locations_horizontal(1)) == 2
    assert len(board.get_available_locations_vertical(1)) == 2


def test_draw_location_std_chosen(monkeypatch):
    board = Board(2, 2)
    monkeypatch.setattr("board.choice", lambda x: x[0])
    drawed_locations = board.draw_location(2)
    assert board.draw_location(1) == [(0, 0)]
    assert drawed_locations == [(0, 0), (1, 0)]
    board.add_warship(drawed_locations)
    assert board.draw_location(1) == [(0, 1)]
    assert board.draw_location(2) == [(0, 1), (1, 1)]


def test_draw_locations_std():
    board = Board(2, 2)
    board.draw_locations()
    assert board.warships() == "2 mast warship 1 mast warship "
    assert len(board.get_available_locations_horizontal(1)) == 1
    assert len(board.get_available_locations_vertical(1)) == 1
    assert board.get_available_locations_horizontal(2) == []
    assert board.get_available_locations_vertical(2) == []


def test_hit_warship_std():
    board = Board(2, 2)
    board.add_warship([(0, 0), (0, 1)])
    assert board.hit((0, 1)) == (True, False, 2)
    board.hit((0, 0)) == (True, True, 2)


def test_hit_warship_out_of_range():
    board = Board(2, 2)
    with pytest.raises(CoordinatesOutOfRangeError):
        board.hit((0, 4))


def test_hit_warship_miss():
    board = Board(2, 2)
    board.add_warship([(0, 0)])
    board.hit((0, 1)) == (False, False, 0)


def test_hit_repeated():
    board = Board(2, 2)
    board.add_warship([(0, 0), (0, 1)])
    board.hit((0, 0)) == (True, False, 2)
    board.hit((0, 0)) == (False, False, 0)


def test_hit_all_sunk_std():
    board = Board(2, 2)
    assert board.all_sunk() is False
    board.add_warship([(0, 0), (0, 1)])
    board.hit((0, 0))
    assert board.all_sunk() is False
    board.hit((0, 1))
    assert board.all_sunk() is True


def test_warships_str_std():
    board = Board(2, 2)
    assert not board.warships_str()
    board.add_warship([(0, 0)])
    assert board.warships_str() == "1 mast warship: x1\n"
    board.add_warship([(1, 0), (1, 1)])
    assert board.warships_str() == "1 mast warship: x1\n2 mast warship: x1\n"
    board.add_warship([(0, 1)])
    assert board.warships_str() == "1 mast warship: x2\n2 mast warship: x1\n"


def test_print_board_std():
    board = Board(2, 2)
    board_str = board.print_board().split("\n")
    assert board_str[0] == "   A  B "
    assert board.print_board() == board.print_board(True)
    board.add_warship([(0, 0)])
    assert "x" not in board.print_board()
    assert "x" not in board.print_board(True)
    assert "o" not in board.print_board()
    assert "o" in board.print_board(True)
    board.hit((0, 1))
    assert "#" in board.print_board()
    assert "#" in board.print_board(True)
    board.hit((0, 0))
    assert "x" in board.print_board()
    assert "x" in board.print_board(True)
