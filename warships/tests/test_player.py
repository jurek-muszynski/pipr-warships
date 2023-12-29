from player import Player, Ai
from board import Board
import pytest


def test_create_player_std():
    board = Board(2, 2)
    player = Player(board)
    assert player.board == board
    assert player.warship_types == {2: 1, 1: 1}


def test_create_player_invalid():
    with pytest.raises(ValueError):
        Player(Board(0, 0))


def test_player_hit_std():
    board = Board(2, 2)
    player = Player(board)
    assert player.hit("A0") == (0, 0)


def test_format_locations_std():
    board = Board(2, 2)
    player = Player(board)
    locations = [[(0, 0), (1, 0)], [(0, 1)]]
    formatted_locations = [["A0", "B0"], ["A1"]]
    assert player._format_locations(locations) == formatted_locations


# def test_place_warships_std(monkeypatch):
#     board = Board(2, 2)
#     player = Player(board)
#     monkeypatch.setattr("player.pick", lambda list, title,
#                         indicator, default_index=0: (0, 0))
#     assert len(board.get_available_locations_horizontal(1)) == 4
#     assert len(board.get_available_locations_vertical(1)) == 4
#     player.place_warships()
#     assert len(board.get_available_locations_horizontal(1)) == 1
#     assert len(board.get_available_locations_vertical(1)) == 1
#     assert board.get_available_locations_vertical(
#         1) == board.get_available_locations_horizontal(1)
#     assert board.get_available_locations_vertical(1) == [[(1, 1)]]


def test_create_ai_player_std():
    board = Board(2, 2)
    ai = Ai(board)
    assert ai.board == board
    assert ai.warship_types == {2: 1, 1: 1}


def test_create_ai_player_invalid():
    with pytest.raises(ValueError):
        Ai(Board(0, 0))


def test_ai_remove_hit_before_no_hits(monkeypatch):
    board = Board(2, 2)
    ai = Ai(board)
    assert ai.remove_hit_before([(0, 0)]) == [(0, 0)]


def test_ai_smart_hit_no_hits(monkeypatch):
    board = Board(2, 2)
    ai = Ai(board)
    monkeypatch.setattr(ai, "draw_coordinates", lambda: (0, 0))
    assert ai.smart_hit() == (0, 0)


# def test_ai_draw_coordinates_std_chosen(monkeypatch):
#     board = Board(2, 2)
#     ai = Ai(board)
#     board.add_warship([(0, 0), (0, 1)])
#     monkeypatch.setattr("player.choice", lambda list: list[0])
#     assert ai.draw_coordinates() == [(1, 0)]
