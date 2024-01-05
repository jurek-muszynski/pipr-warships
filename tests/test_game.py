from classes.game import Game, GameEnded
import pytest


def test_create_game_std():
    """
    Test game's constructor method\n
    This test targets the standard use case
    """
    Game("5")


def test_create_game_invalid():
    """
    Test game's constructor method\n
    This test targets the incorrect use case
    """
    with pytest.raises(ValueError):
        Game("5.22")


def test_game_players_turn_std(monkeypatch):
    """
    Test game's players_turn() method\n
    This test targets the standard use case
    """
    game = Game("2")
    monkeypatch.setattr("classes.game.sleep", lambda _: None)
    monkeypatch.setattr("builtins.input", lambda _: "A0")
    game.players_turn()


def test_game_ai_turn_std(monkeypatch):
    """
    Test game's ai_turn() method\n
    This test targets the standard use case
    """
    game = Game("2")
    monkeypatch.setattr("classes.game.sleep", lambda _: None)
    monkeypatch.setattr("builtins.input", lambda _: "A0")
    game.ai_turn()


def test_game_result_player(monkeypatch):
    """
    Test game's result_player() method\n
    This test targets the standard use case
    """
    game = Game("2")
    monkeypatch.setattr("classes.game.sleep", lambda _: None)
    monkeypatch.setattr("builtins.input", lambda _: "A0")
    game.players_turn()
    game.result_player()


def test_game_result_ai(monkeypatch):
    """
    Test game's result_ai() method\n
    This test targets the standard use case
    """
    game = Game("2")
    monkeypatch.setattr("classes.game.sleep", lambda _: None)
    monkeypatch.setattr("builtins.input", lambda _: "A0")
    game.ai_turn()
    game.result_ai()


def test_game_player_won(monkeypatch):
    """
    Test game's main functionality.\n
    This test targets the case, when the player wins
    """
    game = Game("2")
    monkeypatch.setattr("classes.game.sleep", lambda _: None)
    monkeypatch.setattr("builtins.print", lambda _: None)
    monkeypatch.setattr("builtins.input", lambda _: "A0")
    game.players_turn()
    monkeypatch.setattr("builtins.input", lambda _: "A1")
    game.players_turn()
    monkeypatch.setattr("builtins.input", lambda _: "B0")
    with pytest.raises(GameEnded):
        game.players_turn()
        monkeypatch.setattr("builtins.input", lambda _: "B1")
        game.players_turn()


def test_game_ai_won(monkeypatch):
    """
    Test game's main functionality.\n
    This test targets the case, when the ai wins
    """
    game = Game("2")
    monkeypatch.setattr("classes.player.sleep", lambda _: None)
    monkeypatch.setattr("classes.game.sleep", lambda _: None)
    monkeypatch.setattr("classes.player.pick_location", lambda a, b: 0)
    game.player.place_warships()
    game.ai_turn()
    game.ai_turn()
    with pytest.raises(GameEnded):
        game.ai_turn()
        game.ai_turn()
