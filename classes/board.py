from warship import Warship, Block
from random import randint, choice


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

    :param num_warships: number of warships situated on the board
    :type num_warships: int

    :param locations_warships: locations of the warships
    :type locations_warships: list[Warship]

    :param warship_types: amount of specific warship types on the board
    :type warship_types: dict[int]
    """

    def __init__(self, size: int, num_warships: int, locations_warships: list[Warship] = [], warship_types: dict[int] = {}) -> None:
        if (size < 0):
            raise NegativeValueError(size)
        else:
            self.__size = size
        if (num_warships < 0):
            raise NegativeValueError(num_warships)
        else:
            self.__num_warships = num_warships
        self.__locations_warships = []
        self.__warship_types = warship_types

    def is_available(self, x, y):
        return (x, y) not in self.__locations_warships

    def get_available_locations_horizontal(self, warship_size):
        locations = []
        for x in range(self.__size):
            for y in range(self.__size - warship_size + 1):
                locations_inner = []
                for size in range(warship_size):
                    if self.is_available(x, y+size):
                        locations_inner.append((x, y+size))
                if (len(locations_inner) == warship_size):
                    locations.append(locations_inner)
        return locations

    def get_available_locations_vertical(self, warship_size):
        locations = []
        for x in range(self.__size - warship_size + 1):
            for y in range(self.__size):
                locations_inner = []
                for size in range(warship_size):
                    if self.is_available(x+size, y):
                        locations_inner.append((x+size, y))
                if (len(locations_inner) == warship_size):
                    locations.append(locations_inner)
        return locations

    def draw_location(self, size_to_add: int):
        warship_size = size_to_add
        alignment = choice(["horizontal", "vertical"])
        if alignment == "horizontal":
            available_locations = self.get_available_locations_horizontal(
                warship_size)
            num_of_available_locations = len(available_locations)
            drawed_index = randint(0, num_of_available_locations-1)
            return available_locations[drawed_index]
        else:
            available_locations = self.get_available_locations_vertical(
                warship_size)
            num_of_available_locations = len(available_locations)
            drawed_index = randint(0, num_of_available_locations-1)
            return available_locations[drawed_index]

    def draw_locations(self):
        warships_sizes = [5, 4, 3, 2, 1]
        warships_to_add = 5
        warships_added = 0
        while warships_added < warships_to_add:
            drawed_locations = self.draw_location(
                warships_sizes[warships_added])
            self.add_warship(drawed_locations)
            warships_added += 1

    def add_warship(self, locations) -> None:
        for x, y in locations:
            self.__locations_warships.append((x, y))

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
