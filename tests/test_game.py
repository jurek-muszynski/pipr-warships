from re import L
from board import Board
from game import Game, GameEnded
from player import Player, Ai
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
    monkeypatch.setattr("game.sleep", lambda _: None)
    monkeypatch.setattr("builtins.input", lambda _: "A0")
    game.players_turn()


def test_game_ai_turn_std(monkeypatch):
    """
    Test game's ai_turn() method\n
    This test targets the standard use case
    """
    game = Game("2")
    monkeypatch.setattr("game.sleep", lambda _: None)
    monkeypatch.setattr("builtins.input", lambda _: "A0")
    game.ai_turn()


def test_game_result_player(monkeypatch):
    """
    Test game's result_player() method\n
    This test targets the standard use case
    """
    game = Game("2")
    monkeypatch.setattr("game.sleep", lambda _: None)
    monkeypatch.setattr("builtins.input", lambda _: "A0")
    game.players_turn()
    game.result_player()


def test_game_result_ai(monkeypatch):
    """
    Test game's result_ai() method\n
    This test targets the standard use case
    """
    game = Game("2")
    monkeypatch.setattr("game.sleep", lambda _: None)
    monkeypatch.setattr("builtins.input", lambda _: "A0")
    game.ai_turn()
    game.result_ai()
