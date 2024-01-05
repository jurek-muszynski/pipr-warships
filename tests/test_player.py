from classes.board import Board
from classes.board import CoordinatesOutOfRangeError
from classes.player import Player, Ai
from classes.player import InvalidHitInputError
import pytest


def test_create_player_std():
    """
    Test player's constructor method\n
    This test targets the standard use case
    """
    board = Board(2, 2)
    player = Player(board)
    assert player.board == board
    assert player.warship_types == {2: 1, 1: 1}


def test_create_player_invalid():
    """
    Test player's constructor method\n
    This test targets the incorrect use case
    """
    with pytest.raises(ValueError):
        Player(Board(0, 0))


def test_player_hit_std():
    """
    Test player's hit() method\n
    This test targets the correct use case
    """
    board = Board(2, 2)
    player = Player(board)
    assert player.hit("A0") == (0, 0)


def test_player_hit_invalid_input():
    """
    Test player's hit() method\n
    This test targets the case when passed input
    is incorrect
    """
    board = Board(2, 2)
    player = Player(board)
    with pytest.raises(InvalidHitInputError):
        board.hit(player.hit("AA"))


def test_player_hit_coordinates_out_of_bounds():
    """
    Test player's hit() method\n
    This test targets the case when passed coordinates
    are out of the board's range
    """
    board = Board(2, 2)
    player = Player(board)
    with pytest.raises(CoordinatesOutOfRangeError):
        board.hit(player.hit("A2"))


def test_format_locations_std():
    """
    Test player's _format_locations() method\n
    This test targets the standard use case
    """
    board = Board(2, 2)
    player = Player(board)
    locations = [[(0, 0), (1, 0)], [(0, 1)]]
    formatted_locations = [["A0", "B0"], ["A1"]]
    assert player._format_locations(locations) == formatted_locations


def test_create_ai_player_std():
    """
    Test ai's constructor method\n
    This test targets the standard use case
    """
    board = Board(2, 2)
    ai = Ai(board)
    assert ai.board == board
    assert ai.warship_types == {2: 1, 1: 1}


def test_create_ai_player_invalid():
    """
    Test ai's constructor method\n
    This test targets the incorrect use case
    """
    with pytest.raises(ValueError):
        Ai(Board(0, 0))


def test_ai_remove_hit_before_std(monkeypatch):
    """
    Test ai's remove_hit_before() method\n
    This test targets the standard use case
    """
    board_ai = Board(2, 2)
    board_player = Board(2, 2)
    ai = Ai(board_ai)
    player = Player(board_player)
    monkeypatch.setattr(ai, "draw_coordinates", lambda: (0, 0))
    hit = ai.smart_hit()
    assert hit == (0, 0)
    player.board.hit(hit)
    assert ai.remove_hit_before([(0, 0), (0, 1), (1, 0), (1, 1)]) == [
        (0, 1), (1, 0), (1, 1)]


def test_ai_remove_hit_before_no_hits():
    """
    Test ai's remove_hit_before() method\n
    This test targets the case, when there
    were no hits before
    """
    board = Board(2, 2)
    ai = Ai(board)
    assert ai.remove_hit_before([(0, 0)]) == [(0, 0)]


def test_ai_get_all_possible_locations_none_sunk():
    """
    Test ai's remove_hit_before() method\n
    This test targets the case, when no ships
    have been sunk yet
    """
    board_ai = Board(2, 2)
    board_player = Board(2, 2)
    ai = Ai(board_ai)
    player = Player(board_player)
    player.board.add_warship([(0, 0)])
    player.board.add_warship([(1, 1), (0, 1)])
    assert len(ai.get_all_possible_locations()) == 16


def test_ai_get_all_possible_locations_one_mast_sunk(monkeypatch):
    """
    Test ai's remove_hit_before() method\n
    This test targets the case, when a one mast
    warship has been sunk
    """
    board_ai = Board(2, 2)
    board_player = Board(2, 2)
    ai = Ai(board_ai)
    player = Player(board_player)
    monkeypatch.setattr(ai, "draw_coordinates", lambda: (0, 0))
    player.board.add_warship([(0, 0)])
    player.board.add_warship([(1, 1), (0, 1)])
    hit = player.board.hit(ai.smart_hit())
    ai.set_next_hit(hit)
    assert (ai.get_all_possible_locations()) == [
        (1, 0), (1, 1), (0, 1), (1, 1)]


def test_ai_check_if_not_hit_before(monkeypatch):
    """
    Test ai's check_if_not_hit_before() method\n
    This test targets standard use case
    """
    board_ai = Board(2, 2)
    board_player = Board(2, 2)
    ai = Ai(board_ai)
    player = Player(board_player)
    assert ai.check_if_not_hit_before([(0, 0)])
    monkeypatch.setattr(ai, "draw_coordinates", lambda: (0, 0))
    player.board.hit(ai.smart_hit())
    assert not ai.check_if_not_hit_before([(0, 0)])


def test_ai_smart_hit_no_hits(monkeypatch):
    """
    Test ai's smart_hit() method\n
    This test targets the case, when there
    were no hits before, mocked random drawing
    """
    board = Board(2, 2)
    ai = Ai(board)
    monkeypatch.setattr(ai, "draw_coordinates", lambda: (0, 0))
    assert ai.smart_hit() == (0, 0)


def test_ai_smart_hit_random():
    """
    Test ai's smart_hit() method\n
    This test targets the case, when there
    were no hits before, random drawing
    """
    board_ai = Board(2, 2)
    board_player = Board(2, 2)
    ai = Ai(board_ai)
    player = Player(board_player)
    player.board.add_warship([(0, 0), (0, 1)])
    all_coordinates = [(0, 0), (0, 1), (1, 1), (1, 0)]
    assert ai.smart_hit() in all_coordinates


def test_ai_smart_hit_chosen_hit_warhsip(monkeypatch):
    """
    Test ai's smart_hit() method\n
    This test targets the case, when there
    were no hits before and the randomly
    drawn hit is successful
    """
    board_ai = Board(2, 2)
    board_player = Board(2, 2)
    ai = Ai(board_ai)
    player = Player(board_player)
    player.board.add_warship([(0, 0), (0, 1)])
    monkeypatch.setattr(ai, "draw_coordinates", lambda: (0, 0))
    hit = ai.smart_hit()
    ai.set_next_hit(player.board.hit(hit))
    monkeypatch.undo()
    hit = ai.smart_hit()
    ai.set_next_hit(player.board.hit(hit))
    assert hit in [(0, 1), (1, 0)]


def test_ai_draw_coordinates_random_coors_no_hits_before(monkeypatch):
    """
    Test ai's draw_coordinates() method\n
    This test targets the case, when there
    no hits before
    """
    board = Board(2, 2)
    ai = Ai(board)
    assert ai.draw_coordinates() in [(0, 0), (0, 1), (1, 0), (1, 1)]


def test_ai_draw_coordinates_random_coors_some_hits_before(monkeypatch):
    """
    Test ai's draw_coordinates() method\n
    This test targets the case, when there
    were some hits before
    """
    board = Board(2, 2)
    ai = Ai(board)
    all_coordinates = [(0, 0), (0, 1), (1, 0), (1, 1)]
    hit_before = [(1, 0), (1, 1)]
    available = [hit for hit in all_coordinates if hit not in hit_before]
    assert available == [(0, 0), (0, 1)]
    monkeypatch.setattr(ai, "remove_hit_before", lambda list: available)
    assert ai.draw_coordinates() in available


def test_ai_draw_coordinates_chosen_coors(monkeypatch):
    """
    Test ai's draw_coordinates() method\n
    This test targets the case, when there
    were some hits before and drawing is mocked
    """
    board = Board(2, 2)
    ai = Ai(board)
    all_coordinates = [(0, 0), (0, 1), (1, 0), (1, 1)]
    hit_before = [(1, 0), (1, 1)]
    available = [hit for hit in all_coordinates if hit not in hit_before]
    monkeypatch.setattr(ai, "remove_hit_before", lambda list: available)
    monkeypatch.setattr("classes.player.choice", lambda list: list[0])
    assert ai.draw_coordinates() == (0, 0)


def test_ai_draw_coordinates_no_available(monkeypatch):
    """
    Test ai's draw_coordinates() method\n
    This test targets the case, when there
    are no empty locations left
    """
    board = Board(2, 2)
    ai = Ai(board)
    monkeypatch.setattr(ai, "remove_hit_before", lambda list: [])
    with pytest.raises(IndexError):
        ai.draw_coordinates()


def test_ai_flatten_valid_locations_std():
    """
    Test ai's flatten_valid_locations() method\n
    This test targets the standard use case
    """
    board = Board(2, 2)
    ai = Ai(board)
    hits = []
    locations = [[(0, 0), (0, 1)], [(0, 0), (1, 0)]]
    assert ai.flatten_valid_locations(locations, hits) == [
        (0, 0), (0, 1), (0, 0), (1, 0)]


def test_ai_flatten_valid_locations_hit():
    """
    Test ai's flatten_valid_locations() method\n
    This test targets the case, when there was a hit
    before
    """
    board = Board(2, 2)
    ai = Ai(board)
    hits = [(0, 0)]
    locations = [[(0, 0), (0, 1)], [(0, 0), (1, 0)]]
    assert ai.flatten_valid_locations(locations, hits) == [(0, 1), (1, 0)]


def test_ai_flatten_valid_locations_one_distinct():
    """
    Test ai's flatten_valid_locations() method\n
    This test targets the case, when there would be
    only one distict location left
    """
    board = Board(2, 2)
    ai = Ai(board)
    hits = [(0, 0), (0, 1)]
    locations = [[(0, 0), (0, 1)], [(0, 0), (1, 0)]]
    assert ai.flatten_valid_locations(locations, hits) == [(1, 0)]


def test_ai_get_next_possible_locations_one_hit_no_misses():
    """
    Test ai's get_next_possible_locations() method\n
    This test targets the case, when there was a single
    hit before without any misses
    """
    board_ai = Board(3, 3)
    board_player = Board(3, 3)
    ai = Ai(board_ai)
    player = Player(board_player)
    player.board.add_warship([(1, 0), (1, 1)])
    size = 2
    hits_size_2 = [(1, 1)]
    possible_next_locs = [(0, 1), (1, 0), (1, 2), (2, 1)]
    assert len(ai.get_next_possible_locations(size, hits_size_2)) == 4
    assert sorted(ai.get_next_possible_locations(
        size, hits_size_2), key=lambda coors: coors[0]) == possible_next_locs


def test_ai_get_next_possible_locations_two_hits_no_misses():
    """
    Test ai's get_next_possible_locations() method\n
    This test targets the case, when there were two
    hits before without any misses
    """
    board_ai = Board(3, 3)
    board_player = Board(3, 3)
    ai = Ai(board_ai)
    player = Player(board_player)
    player.board.add_warship([(0, 0), (1, 0), (2, 0)])
    size = 3
    hits_size_3 = [(0, 0), (1, 0)]
    possible_next_locations = [(2, 0)]
    assert ai.get_next_possible_locations(
        size, hits_size_3) == possible_next_locations


def test_ai_get_next_possible_locations_one_hit_some_misses(monkeypatch):
    """
    Test ai's get_next_possible_locations() method\n
    This test targets the case, when there was a single
    hit with some misses
    """
    board_ai = Board(3, 3)
    board_player = Board(3, 3)
    ai = Ai(board_ai)
    player = Player(board_player)
    player.board.add_warship([(1, 0), (1, 1)])
    size = 2
    hits_size_2 = [(1, 1)]
    misses = [(2, 1), (1, 2)]
    possible_next_locations = [(1, 0), (0, 1)]
    monkeypatch.setattr(ai, "draw_coordinates", lambda: misses[0])
    ai.smart_hit()
    monkeypatch.undo()
    monkeypatch.setattr(ai, "draw_coordinates", lambda: misses[1])
    ai.smart_hit()
    monkeypatch.undo()
    assert ai.get_next_possible_locations(
        size, hits_size_2) == possible_next_locations


def test_ai_get_next_possible_locations_some_hit_no_misses(monkeypatch):
    """
    Test ai's get_next_possible_locations() method\n
    This test targets the case, when there were some
    hits before without any misses
    """
    board_ai = Board(3, 3)
    board_player = Board(3, 3)
    ai = Ai(board_ai)
    player = Player(board_player)
    player.board.add_warship([(1, 0), (1, 1)])
    player.board.add_warship([(0, 1)])
    size = 2
    hits_size_2 = [(1, 1)]
    hits_overall = [(0, 1), (1, 1)]
    monkeypatch.setattr(ai, "draw_coordinates", lambda: hits_overall[0])
    ai.smart_hit()
    monkeypatch.undo()
    monkeypatch.setattr(ai, "draw_coordinates", lambda: hits_overall[1])
    ai.smart_hit()
    next_possible_locations = [(1, 0), (1, 2), (2, 1)]
    assert ai.get_next_possible_locations(
        size, hits_size_2) == next_possible_locations


def test_ai_set_next_hit_with_key_chosen(monkeypatch):
    """
    Test ai's set_next_hit_with_key() method\n
    This test targets the standard use case,
    mocked random drawing
    """
    board = Board(3, 3)
    ai = Ai(board)
    hit_size = 2
    monkeypatch.setattr(ai, "get_next_possible_locations", lambda size, hits: [
                        [(0, 1)], [(1, 2)], [(2, 1)], [(1, 0)]])
    monkeypatch.setattr("classes.player.choice",
                        lambda locations: locations[0])
    assert ai.set_next_hit_with_key(hit_size) == [(0, 1)]


def test_ai_set_next_hit_with_key_random(monkeypatch):
    """
    Test ai's set_next_hit_with_key() method\n
    This test targets the standard use case,
    mocked random
    """
    board = Board(3, 3)
    ai = Ai(board)
    hit_size = 2
    monkeypatch.setattr(ai, "get_next_possible_locations", lambda size, hits: [
                        [(0, 1)], [(1, 2)], [(2, 1)], [(1, 0)]])
    assert len(ai.set_next_hit_with_key(hit_size)) == 1


def test_ai_set_next_hit_success(monkeypatch):
    """
    Test the ai.set_next_hit() method.\n
    This test targets the case when last hit was
    successful
    """
    board_ai = Board(3, 3)
    board_player = Board(3, 3)
    ai = Ai(board_ai)
    player = Player(board_player)
    player.board.add_warship([(0, 0), (0, 1)])
    player.board.add_warship([(1, 0), (1, 1), (1, 2)])
    monkeypatch.setattr(ai, "draw_coordinates", lambda: (0, 0))
    hit = ai.smart_hit()
    assert hit == (0, 0)
    monkeypatch.undo()
    hit_result = player.board.hit(hit)
    assert hit_result == (True, False, 2)
    ai.set_next_hit(hit_result)
    hit = ai.smart_hit()
    assert hit in [(0, 1), (1, 0)]


def test_ai_set_next_hit_miss_and_draw_coordinates(monkeypatch):
    """
    Test the ai.set_next_hit() method.\n
    This test targets the case when last hit
    was missed and there were no successful hits before
    """
    board_ai = Board(2, 2)
    board_player = Board(2, 2)
    ai = Ai(board_ai)
    player = Player(board_player)
    player.board.add_warship([(0, 0), (0, 1)])
    monkeypatch.setattr(ai, "draw_coordinates", lambda: (1, 1))
    hit = ai.smart_hit()
    assert hit == (1, 1)
    monkeypatch.undo()
    hit_result = player.board.hit(hit)
    assert hit_result == (False, False, 0)
    ai.set_next_hit(hit_result)
    hit = ai.smart_hit()
    left_coordinates = [(0, 0), (0, 1), (1, 0)]
    assert hit in left_coordinates


def test_ai_set_next_hit_miss_and_last_success_hit(monkeypatch):
    """
    Test the ai.set_next_hit() method.\n
    This test targets the case when last hit
    was missed and there was a successful hit before
    """
    board_ai = Board(2, 2)
    board_player = Board(2, 2)
    ai = Ai(board_ai)
    player = Player(board_player)
    player.board.add_warship([(0, 0), (0, 1)])
    monkeypatch.setattr(ai, "draw_coordinates", lambda: (0, 1))
    hit = ai.smart_hit()
    assert hit == (0, 1)
    monkeypatch.undo()
    hit_result = player.board.hit(hit)
    assert hit_result == (True, False, 2)
    monkeypatch.setattr(ai, "set_next_hit_with_key", lambda key: (1, 1))
    ai.set_next_hit(hit_result)
    hit = ai.smart_hit()
    assert hit == (1, 1)
    monkeypatch.undo()
    hit_result = player.board.hit(hit)
    assert hit_result == (False, False, 0)
    ai.set_next_hit(hit_result)
    hit = ai.smart_hit()
    assert hit == (0, 0)


def test_ai_set_next_hit_sink_and_last_success_hit(monkeypatch):
    """
    Test the ai.set_next_hit() method.\n
    This test targets the case when last hit sank
    a warship and there was a successful hit at a
    different warship before\n
    """
    board_ai = Board(3, 3)
    board_player = Board(3, 3)
    ai = Ai(board_ai)
    player = Player(board_player)
    player.board.add_warship([(0, 0), (0, 1)])
    player.board.add_warship([(1, 0), (1, 1), (1, 2)])
    monkeypatch.setattr(ai, "draw_coordinates", lambda: (1, 0))
    hit = ai.smart_hit()
    assert hit == (1, 0)
    monkeypatch.undo()
    hit_result = player.board.hit(hit)
    assert hit_result == (True, False, 3)
    monkeypatch.setattr(ai, "set_next_hit_with_key", lambda key: (0, 0))
    ai.set_next_hit(hit_result)
    hit = ai.smart_hit()
    assert hit == (0, 0)
    monkeypatch.undo()
    hit_result = player.board.hit(hit)
    assert hit_result == (True, False, 2)
    ai.set_next_hit(hit_result)
    hit = ai.smart_hit()
    assert hit == (0, 1)
    hit_result = player.board.hit(hit)
    assert hit_result == (True, True, 2)
    ai.set_next_hit(hit_result)
    hit = ai.smart_hit()
    assert hit in [(1, 1), (1, 2)]


def test_ai_set_next_hit_sink_and_draw_coordinates(monkeypatch):
    """
    Test the ai.set_next_hit() method.\n
    This test targets the case when last hit sank
    a warship and there were no successful hits at
    different warships before\n
    """
    board_ai = Board(3, 3)
    board_player = Board(3, 3)
    ai = Ai(board_ai)
    player = Player(board_player)
    player.board.add_warship([(0, 0), (0, 1)])
    player.board.add_warship([(1, 0), (1, 1), (1, 2)])
    monkeypatch.setattr(ai, "draw_coordinates", lambda: (0, 0))
    hit = ai.smart_hit()
    assert hit == (0, 0)
    monkeypatch.undo()
    hit_result = player.board.hit(hit)
    assert hit_result == (True, False, 2)
    monkeypatch.setattr(ai, "set_next_hit_with_key", lambda key: (0, 1))
    ai.set_next_hit(hit_result)
    hit = ai.smart_hit()
    assert hit == (0, 1)
    monkeypatch.undo()
    hit_result = player.board.hit(hit)
    assert hit_result == (True, True, 2)
    ai.set_next_hit(hit_result)
    hit = ai.smart_hit()
    assert hit in [(0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
