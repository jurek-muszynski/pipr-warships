from board import Board, CoordinatesOutOfRangeError
from player import Player, Ai
from time import sleep
from os import system
from consts import MAX_NUM_OF_WARSHIPS
from system import clear


class GameEnded(Exception):
    pass


class Game():
    """

    """

    def __init__(self, board_size: int) -> None:
        self.__board_size = board_size
        self.__player = Player(
            Board(self.__board_size, self.__board_size
                  if self.__board_size < MAX_NUM_OF_WARSHIPS
                  else MAX_NUM_OF_WARSHIPS))
        self.__ai = Ai(
            Board(self.__board_size, self.__board_size
                  if self.__board_size < MAX_NUM_OF_WARSHIPS
                  else MAX_NUM_OF_WARSHIPS))
        self.__ai.board.draw_locations()

    def players_turn(self):
        print("\nYOUR TURN")
        sleep(1)
        print(self.__ai.board.warships_str())
        print("AI's BOARD")
        print(self.__ai.board.print_board())
        while True:
            try:
                hit = self.__player.hit(
                    input("Where would you like to hit: "))
                self.__ai.board.hit(hit)
                break
            except CoordinatesOutOfRangeError as e:
                print(str(e))
            except Exception:
                print("Invalid input")
        self.result_player()

    def ai_turn(self):
        print("\nAI'S TURN")
        sleep(1)
        print("YOUR BOARD")
        print(self.__player.board.print_board(True))
        hit = self.__ai.smart_hit()
        print(chr(int(hit[0])+65) + str(hit[1]))
        sleep(1)
        self.__ai.set_last_hit(self.__player.board.hit(hit))
        self.result_ai()

    def result_player(self):
        if self.__ai.board.all_sunk():
            sleep(1)
            clear()
            sleep(1)
            print("ALL AI'S SHIPS SANK")
            sleep(1)
            clear()
            sleep(1)
            print("YOU'VE WON!")
            raise GameEnded()
        sleep(1)

    def result_ai(self):
        if self.__player.board.all_sunk():
            sleep(1)
            clear()
            print("ALL YOUR SHIPS SANK!")
            sleep(1)
            clear()
            sleep(1)
            print("YOU'VE LOST")
            raise GameEnded()
        sleep(1)

    def play(self):
        self.__player.place_warships()
        while True:
            try:
                self.players_turn()
                self.ai_turn()
            except GameEnded:
                sleep(1)
                clear()
                break
