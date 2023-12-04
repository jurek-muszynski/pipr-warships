from warship import Warship, Block
from random import randint


class NegativeValueError(Exception):
    """
    NegativeValueError Exception.
    Raised when negative value was passed as a parameter (size, num_warships)

    :param value: passed value
    :type value: int
    """

    def __init__(self, value: int) -> None:
        super().__init__("This value cannot be negative")
        self.__value = value


class Board():
    """
    Board class. Contains attributes:

    :param size: number of either rows/columns, as the board is a square
    :type size: int

    :param num_warships: number of warships situated at the board
    :type num_warships: int

    :param locations_warships: locations of the warships
    :type locations_warships: list[Warship]
    """

    def __init__(self, size: int, num_warships: int, locations_warships: list[Warship] = []) -> None:
        if (size < 0):
            raise NegativeValueError(size)
        else:
            self.__size = size
        if (num_warships < 0):
            raise NegativeValueError(num_warships)
        else:
            self.__num_warships = num_warships
        self.__locations_warships = []

    def draw_location(self) -> Block:
        x_coordinate = randint(0, self.__size-1)
        y_coordinate = randint(0, self.__size-1)
        # block = Block(x_coordinate, y_coordinate)
        return (x_coordinate, y_coordinate)

    def draw_locations(self):
        blocks_added = 0
        while blocks_added < self.__num_warships:
            block_to_add = self.draw_location()
            if block_to_add not in self.__locations_warships:
                self.add_location(block_to_add)
                blocks_added += 1

    def add_location(self, location: Block) -> None:
        self.__locations_warships.append(location)

    def print_legend_horizontal(self) -> str:
        legend_horizontal = [chr(num+65) for num in range(0, self.__size)]
        legend_horizontal_as_str = "  "
        for letter in legend_horizontal:
            legend_horizontal_as_str += f"{letter:^3}"
        return legend_horizontal_as_str

    def print_board(self) -> str:
        board_str = self.print_legend_horizontal()
        board_str += "\n"
        for index in range(self.__size):
            board_str += f"{index} "
            for index_inner in range(self.__size):
                if (index_inner, index) not in self.__locations_warships:
                    board_str += "[ ]"
                else:
                    board_str += "[x]"
            board_str += "\n"
        return board_str
