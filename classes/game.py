from board import Board
from game_io import modify_hit_input
from time import sleep


class Game():
    """

    """

    def __init__(self, board_size: int, warships: int) -> None:
        self.__board_size = board_size
        self.__warships = warships
        self.__board = Board(self.__board_size, self.__warships)

    def play(self):
        self.__board.draw_locations()
        print(self.__board.print_board())
        while True:
            print(self.__board.drawed_warships_str())

            hit = modify_hit_input(
                input("Where would you like to hit > "))
            print(self.__board.hit(hit))
            sleep(0.5)
            print(self.__board.print_board())
            if (self.__board.all_sunk()):
                print("All warships had been sunk")
                sleep(0.5)
                break
