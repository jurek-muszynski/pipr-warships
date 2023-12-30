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


def test_ai_draw_coordinates_std_random_coors(monkeypatch):
    board = Board(2, 2)
    ai = Ai(board)
    hit_before = [(1, 0), (1, 1)]
    monkeypatch.setattr(ai, "remove_hit_before", lambda list: hit_before)
    assert ai.draw_coordinates() in hit_before


def test_ai_draw_coordinates_std_chosen_coors(monkeypatch):
    board = Board(2, 2)
    ai = Ai(board)
    hit_before = [(1, 0), (1, 1)]
    monkeypatch.setattr(ai, "remove_hit_before", lambda list: hit_before)
    monkeypatch.setattr("player.choice", lambda list: list[0])
    assert ai.draw_coordinates() == (1, 0)


def test_ai_draw_coordinates_warships_coors(monkeypatch):
    board = Board(2, 2)
    ai = Ai(board)
    warships_coors = [(0, 0), (0, 1)]
    board.add_warship(warships_coors)
    warships = {
        2: warships_coors
    }
    monkeypatch.setattr(ai, "_Ai__warships_hit", warships)
    assert ai.draw_coordinates() not in warships_coors
    assert ai.draw_coordinates() in [(1, 0), (1, 1)]


def test_ai_draw_coordinates_no_available(monkeypatch):
    board = Board(2, 2)
    ai = Ai(board)
    monkeypatch.setattr(ai, "remove_hit_before", lambda list: [])
    with pytest.raises(IndexError):
        ai.draw_coordinates()


def test_ai_flatten_valid_locations_std():
    board = Board(2, 2)
    ai = Ai(board)
    hits = [(0, 0)]
    locations = [[(0, 0), (0, 1)], [(0, 0), (1, 0)]]
    assert ai.flatten_valid_locations(locations, hits) == [(0, 1), (1, 0)]


def test_ai_flatten_valid_locations_single_distinct():
    board = Board(2, 2)
    ai = Ai(board)
    hits = [(0, 0), (0, 1)]
    locations = [[(0, 0), (0, 1)], [(0, 0), (1, 0)]]
    assert ai.flatten_valid_locations(locations, hits) == [(1, 0)]


def test_ai_get_next_possible_locations_one_hit_no_misses():
    board = Board(3, 3)
    ai = Ai(board)
    board.add_warship([(1, 0), (1, 1)])
    size = 2
    hits_size_2 = [(1, 1)]
    possible_next_locs = [(0, 1), (1, 0), (1, 2), (2, 1)]
    assert len(ai.get_next_possible_locations(size, hits_size_2)) == 4
    assert sorted(ai.get_next_possible_locations(
        size, hits_size_2), key=lambda coors: coors[0]) == possible_next_locs


def test_ai_get_next_possible_locations_two_hits_no_misses():
    board = Board(3, 3)
    ai = Ai(board)
    board.add_warship([(0, 0), (1, 0), (2, 0)])
    size = 3
    hits_size_3 = [(0, 0), (1, 0)]
    possible_next_locations = [(2, 0)]
    assert ai.get_next_possible_locations(
        size, hits_size_3) == possible_next_locations


def test_ai_get_next_possible_locations_one_hit_some_misses(monkeypatch):
    board = Board(3, 3)
    ai = Ai(board)
    board.add_warship([(1, 0), (1, 1)])
    size = 2
    hits_size_2 = [(1, 1)]
    misses = [(2, 1), (1, 2)]
    possible_next_locations = [(1, 0), (0, 1)]
    monkeypatch.setattr(ai, "_Ai__hit", misses)
    assert ai.get_next_possible_locations(
        size, hits_size_2) == possible_next_locations


def test_ai_get_next_possible_locations_some_hit_no_misses(monkeypatch):
    board = Board(3, 3)
    ai = Ai(board)
    board.add_warship([(1, 0), (1, 1)])
    board.add_warship([(0, 1)])
    size = 2
    hits_size_2 = [(1, 1)]
    hits_overall = [(0, 1), (1, 1)]
    monkeypatch.setattr(ai, "_Ai__hit", hits_overall)
    next_possible_locations = [(1, 0), (1, 2), (2, 1)]
    assert ai.get_next_possible_locations(
        size, hits_size_2) == next_possible_locations


def test_ai_get_next_hit_with_key_std(monkeypatch):
    board = Board(3, 3)
    ai = Ai(board)
    hit_size = 2
    monkeypatch.setattr(ai, "get_next_possible_locations", lambda size, hits: [
                        [(0, 1)], [(1, 2)], [(2, 1)], [(1, 0)]])
    monkeypatch.setattr("player.choice", lambda locations: locations[0])
    assert ai.set_next_hit_with_key(hit_size) == [(0, 1)]


def test_ai_get_next_hit_with_key_random(monkeypatch):
    board = Board(3, 3)
    ai = Ai(board)
    hit_size = 2
    monkeypatch.setattr(ai, "get_next_possible_locations", lambda size, hits: [
                        [(0, 1)], [(1, 2)], [(2, 1)], [(1, 0)]])
    assert len(ai.set_next_hit_with_key(hit_size)) == 1


def test_ai_set_next_hit_miss_draw_coordinates():
    board = Board(2, 2)
    all_coordinates = [(0, 0), (0, 1), (1, 1), (1, 0)]
    ai = Ai(board)
    hit_result = (False, False, 0)
    ai.set_next_hit(hit_result)
    assert ai._Ai__next_hit in all_coordinates


def test_ai_set_next_hit_miss_success_hits(monkeypatch):
    board = Board(2, 2)
    ai = Ai(board)
    hit_result = (False, False, 0)
    hits_size_2 = [(1, 1)]
    monkeypatch.setattr(ai, "_Ai__success_hit", hits_size_2)
