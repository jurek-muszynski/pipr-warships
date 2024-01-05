from board import Board
from board import CoordinatesOutOfRangeError
from player import Player, Ai
from player import InvalidHitInputError
from time import sleep
from consts import MAX_NUM_OF_WARSHIPS
from system_io import clear


class GameEnded(Exception):
    """
    GameEnded Exception.\n
    Raised if one of the players has sunk all
    of the oponent's warships
    """
    pass


class Game():
    """
    Game class. Contains attributes:

    :param board_size: board's size
    :type board_size: int

    :param player: a player, the user plays as
    :type player: Player

    :param ai: a player, the user plays against
    :type ai: Ai
    """

    def __init__(self, board_size: int) -> None:
        """
        Creates an instance of the Game class.\n
        Randomly draws locations for the Ai's warships

        :param board_size: board's size
        :type board_size: int
        """
        self.__board_size = int(board_size)
        self.__player = Player(
            Board(self.__board_size, self.__board_size
                  if self.__board_size < MAX_NUM_OF_WARSHIPS
                  else MAX_NUM_OF_WARSHIPS))
        self.__ai = Ai(
            Board(self.__board_size, self.__board_size
                  if self.__board_size < MAX_NUM_OF_WARSHIPS
                  else MAX_NUM_OF_WARSHIPS))
        self.__ai.board.draw_locations()

    @property
    def player(self) -> Player:
        return self.__player

    def players_turn(self) -> None:
        """
        Lets the player choose locations for next hits.\n
        Raises CoordinatesOutOfRangeError if chosen coordinates
        are out of the board's bounds.\n
        Raises InvalidHitInputError if entered hit is invalid.
        """
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
            except InvalidHitInputError as e:
                print(str(e))
        sleep(1)
        print(self.__ai.board.print_board())
        sleep(1)
        self.result_player()

    def ai_turn(self) -> None:
        """
        Lets the Ai make hits\n
        """
        print("\nAI'S TURN")
        sleep(1)
        hit = self.__ai.smart_hit()
        print(chr(int(hit[0])+65) + str(hit[1]))
        sleep(1)
        self.__ai.set_next_hit(self.__player.board.hit(hit))
        sleep(1)
        print("\nYOUR BOARD")
        print(self.__player.board.print_board(True))
        sleep(1)
        self.result_ai()

    def result_player(self) -> None:
        """
        Prints the result of the game if all
        Ai's ships have been sunk.\n

        Raises GameEnded Exception if the player has won
        """
        if self.__ai.board.all_sunk():
            sleep(1)
            clear()
            sleep(1)
            print("ALL AI'S SHIPS HAVE BEEN SANK")
            sleep(2)
            clear()
            sleep(1)
            print("YOU'VE WON!")
            sleep(1)
            raise GameEnded()
        sleep(1)

    def result_ai(self) -> None:
        """
        Prints the result of the game if all
        player's ships have been sunk

        Raises GameEnded Exception if the Ai has won
        """
        if self.__player.board.all_sunk():
            sleep(1)
            clear()
            sleep(1)
            print("ALL YOUR SHIPS HAVE BEEN SANK!")
            sleep(2)
            clear()
            sleep(1)
            print("YOU'VE LOST")
            sleep(1)
            raise GameEnded()
        sleep(1)

    def play(self) -> None:
        """
        Main game loop.\n
        Allows the user to place their warships.\n
        Exchanges turns between the player and the Ai until
        GameEnded Exception is raised
        """
        round = 1
        self.__player.place_warships()
        while True:
            try:
                print(f"Round {round}.")
                self.players_turn()
                self.ai_turn()
                clear()
                round += 1
            except GameEnded:
                sleep(1)
                clear()
                break
