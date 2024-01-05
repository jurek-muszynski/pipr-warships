from classes.board import Board
from classes.board import (InvalidWarshipCountError, InvalidWarshipError,
                           CoordinatesOutOfRangeError)
import pytest


def test_create_board_std():
    """
    Test board's constructor method\n
    This test targets the standard use case
    """
    board = Board(4, 4)
    assert board.size == 4
    assert board.num_warships == 4
    assert not board.warships()


def test_create_board_invalid():
    """
    Test board's constructor method\n
    This test targets the incorrect use cases
    """
    with pytest.raises(ValueError):
        Board(0, 1)
    with pytest.raises(ValueError):
        Board(27, 1)
    with pytest.raises(InvalidWarshipCountError):
        Board(1, 0)
    with pytest.raises(ValueError):
        Board(-10, 5)
    with pytest.raises(InvalidWarshipCountError):
        Board(1, -1)
    with pytest.raises(InvalidWarshipCountError):
        Board(4, 5)


def test_board_all_locations():
    """
    Test board's all_locations() method\n
    This test targets the standard use case
    """
    board1 = Board(1, 1)
    assert board1.all_locations() == [(0, 0)]
    board2 = Board(2, 2)
    assert board2.all_locations() == [(0, 0), (0, 1), (1, 0), (1, 1)]


def test_board_add_warship_std():
    """
    Test board's add_warship() method\n
    This test targets the standard use case
    """
    board = Board(4, 4)
    blocks = [(0, 0), (0, 1), (0, 2), (0, 3)]
    board.add_warship(blocks)
    assert board.warships() == "4 mast warship "


def test_board_add_warship_invalid():
    """
    Test board's add_warship() method\n
    This test targets the incorrect use cases,
    when a warship cannot be added
    """
    board = Board(4, 4)
    blocks = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]
    with pytest.raises(InvalidWarshipError):
        board.add_warship(blocks)
    with pytest.raises(InvalidWarshipError):
        board.add_warship([(0, 4)])
    board.add_warship([(0, 0)])
    with pytest.raises(InvalidWarshipError):
        board.add_warship([(0, 0), (0, 1)])


def test_board_is_location_available():
    """
    Test board's _is_location_available() method\n
    This test targets the standard use case
    """
    board = Board(2, 2)
    assert board._is_location_available(0, 0)
    board.add_warship([(0, 0)])
    assert not board._is_location_available(0, 0)


def test_board_get_available_locations_horizontal_std():
    """
    Test board's get_available_locations_horizontal() method\n
    This test targets the standard use case
    """
    board = Board(2, 2)
    blocks_1 = [[(0, 0)], [(0, 1)], [(1, 0)], [(1, 1)]]
    blocks_2 = [[(0, 0), (0, 1)], [(1, 0), (1, 1)]]
    assert board.get_available_locations_horizontal(1) == blocks_1
    assert board.get_available_locations_horizontal(2) == blocks_2


def test_board_get_available_locations_vertical_std():
    """
    Test board's get_available_locations_vertical() method\n
    This test targets the standard use case
    """
    board = Board(2, 2)
    blocks_1 = [[(0, 0)], [(0, 1)], [(1, 0)], [(1, 1)]]
    blocks_2 = [[(0, 0), (1, 0)], [(0, 1), (1, 1)]]
    assert board.get_available_locations_vertical(1) == blocks_1
    assert board.get_available_locations_vertical(2) == blocks_2


def test_board_get_available_locations_horizontal_added_warships():
    """
    Test board's get_available_locations_horizontal() method\n
    This test targets the case, when some locations are already
    occupied by a warship
    """
    board = Board(2, 2)
    blocks1 = [[(1, 0)], [(1, 1)]]
    blocks2 = [[(1, 0), (1, 1)]]
    board.add_warship([(0, 0), (0, 1)])
    assert board.get_available_locations_horizontal(1) == blocks1
    assert board.get_available_locations_horizontal(2) == blocks2


def test_board_get_available_locations_vertical_added_warships():
    """
    Test board's get_available_locations_vertical() method\n
    This test targets the case, when some locations are already
    occupied by a warship
    """
    board = Board(2, 2)
    blocks1 = [[(0, 1)], [(1, 1)]]
    blocks2 = [[(0, 1), (1, 1)]]
    board.add_warship([(0, 0), (1, 0)])
    assert board.get_available_locations_vertical(1) == blocks1
    assert board.get_available_locations_vertical(2) == blocks2


def test_board_get_available_locations_horizontal_no_available():
    """
    Test board's get_available_locations_horizontal() method\n
    This test targets the case, there are no available locations
    left
    """
    board = Board(2, 2)
    board.add_warship([(0, 0), (0, 1)])
    board.add_warship([(1, 0), (1, 1)])
    assert board.get_available_locations_horizontal(1) == []
    assert board.get_available_locations_horizontal(2) == []


def test_board_get_available_locations_vertical_no_available():
    """
    Test board's get_available_locations_vertical() method\n
    This test targets the case, there are no available locations
    left
    """
    board = Board(2, 2)
    board.add_warship([(0, 0), (1, 0)])
    board.add_warship([(0, 1), (1, 1)])
    assert board.get_available_locations_vertical(1) == []
    assert board.get_available_locations_vertical(2) == []


def test_board_draw_location_std_random():
    """
    Test board's draw_location() method\n
    This test targets the standard use case, randomly drawn location
    """
    board = Board(2, 2)
    drawed_locations = board.draw_location(2)
    assert drawed_locations is not None
    assert len(board.get_available_locations_horizontal(1)) == 4
    assert len(board.get_available_locations_vertical(1)) == 4
    board.add_warship(drawed_locations)
    assert len(board.get_available_locations_horizontal(1)) == 2
    assert len(board.get_available_locations_vertical(1)) == 2


def test_board_draw_location_std_chosen(monkeypatch):
    """
    Test board's draw_location() method\n
    This test targets the standard use case, mocked drawn location
    """
    board = Board(2, 2)
    monkeypatch.setattr("classes.board.choice", lambda x: x[0])
    drawed_locations = board.draw_location(2)
    assert board.draw_location(1) == [(0, 0)]
    assert drawed_locations == [(0, 0), (1, 0)]
    board.add_warship(drawed_locations)
    assert board.draw_location(1) == [(0, 1)]
    assert board.draw_location(2) == [(0, 1), (1, 1)]


def test_board_draw_locations_std():
    """
    Test board's draw_locations() method\n
    This test targets the standard use case
    """
    board = Board(2, 2)
    board.draw_locations()
    assert board.warships() == "2 mast warship 1 mast warship "
    assert len(board.get_available_locations_horizontal(1)) == 1
    assert len(board.get_available_locations_vertical(1)) == 1
    assert board.get_available_locations_horizontal(2) == []
    assert board.get_available_locations_vertical(2) == []


def test_board_hit_warship_success():
    """
    Test board's hit_warship() method\n
    This test targets the case, when a hit was successful
    and didn't sink a warship
    """
    board = Board(2, 2)
    board.add_warship([(0, 0), (0, 1)])
    assert board.hit((0, 1)) == (True, False, 2)


def test_board_hit_warship_sink():
    """
    Test board's hit_warship() method\n
    This test targets the case, when hits were successful
    and eventually sank a warship
    """
    board = Board(2, 1)
    board.add_warship([(0, 0), (0, 1)])
    assert board.hit((0, 1)) == (True, False, 2)
    assert board.hit((0, 0)) == (True, True, 2)


def test_board_hit_warship_out_of_range():
    """
    Test board's hit_warship() method\n
    This test targets the case, when a hit
    is out of the board's range
    """
    board = Board(2, 2)
    with pytest.raises(CoordinatesOutOfRangeError):
        board.hit((0, 4))


def test_board_hit_warship_miss():
    """
    Test board's hit_warship() method\n
    This test targets the case, when a hit was
    a miss
    """
    board = Board(2, 2)
    board.add_warship([(0, 0)])
    assert board.hit((0, 1)) == (False, False, 0)


def test_board_hit_repeated():
    """
    Test board's hit_warship() method\n
    This test targets the case, when hits were
    repeated
    """
    board = Board(2, 2)
    board.add_warship([(0, 0), (0, 1)])
    assert board.hit((0, 0)) == (True, False, 2)
    assert board.hit((0, 0)) == (False, False, 0)


def test_board_hit_all_sunk_std():
    """
    Test board's all_sunk() method\n
    This test targets the standard use case
    """
    board = Board(2, 2)
    assert board.all_sunk() is False
    board.add_warship([(0, 0), (0, 1)])
    board.hit((0, 0))
    assert board.all_sunk() is False
    board.hit((0, 1))
    assert board.all_sunk() is True


def test_board_warships_str_std():
    """
    Test board's warships_str() method\n
    This test targets the standard use case
    """
    board = Board(2, 2)
    assert not board.warships_str()
    board.add_warship([(0, 0)])
    assert board.warships_str() == "1 mast warship: x1\n"
    board.add_warship([(1, 0), (1, 1)])
    assert board.warships_str() == "1 mast warship: x1\n2 mast warship: x1\n"
    board.add_warship([(0, 1)])
    assert board.warships_str() == "1 mast warship: x2\n2 mast warship: x1\n"


def test_board_print_board_std():
    """
    Test board's print_board() method\n
    This test targets the standard use case
    """
    board = Board(2, 2)
    board_str = board.print_board().split("\n")
    assert board_str[0] == "    A  B "
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
