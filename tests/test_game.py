from game import Game
import pytest


def test_create_game_std():
    Game("5")


def test_create_game_invalid():
    with pytest.raises(ValueError):
        Game("5.22")


def test_game_players_turn_std(monkeypatch):
    game = Game("2")
    monkeypatch.setattr("game.sleep", lambda _: None)
    monkeypatch.setattr("builtins.input", lambda _: "A0")
    game.players_turn()
