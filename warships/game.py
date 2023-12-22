from board import Board
from player import Player, Ai
from time import sleep


class Game():
    """

    """

    def __init__(self, board_size: int) -> None:
        self.__board_size = board_size
        self.__player = Player(
            Board(self.__board_size, self.__board_size))
        self.__ai = Player(Board(self.__board_size, self.__board_size))
        self.__ai.board.draw_locations()
        self.__has_ended = False

    def players_turn(self):
        print("AI's BOARD")
        print(self.__ai.board.print_board())
        hit = self.__player.hit(
            input("Where would you like to hit > "))
        self.__ai.board.hit(hit)
        print("AI'S BOARD")
        print(self.__ai.board.print_board())
        self.result_player()

    def ai_turn(self):
        print("YOUR BOARD")
        print(self.__player.board.print_board())
        hit = self.__ai.hit(
            input("Where would the AI like to hit > "))
        self.__player.board.hit(hit)
        print("YOUR BOARD")
        print(self.__player.board.print_board())
        self.result_ai()

    def result_player(self):
        if self.__ai.board.all_sunk():
            print("ALL AI'S SHIPS SANK")
            sleep(0.5)
            print("YOU'VE WON!")
            self.__has_ended = True

    def result_ai(self):
        if self.__player.board.all_sunk():
            print("ALL YOUR SHIPS SANK!")
            sleep(0.5)
            print("YOU'VE LOST")
            self.__has_ended = True

    def play(self):
        self.__player.place_warships()
        while not self.__has_ended:
            self.players_turn()
            self.ai_turn()
            sleep(0.5)
