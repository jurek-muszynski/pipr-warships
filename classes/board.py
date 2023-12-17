from warship import Warship
from board_io import print_board_io, print_drawed_warships_io, print_hit_warships_io
from random import choice


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


class InvalidWarshipCountError(Exception):
    """
    InvalidWarshipCountError Exception.
    Raised when this many warships cannot be placed on the board

    :param value: passed value
    :type value: int

    """

    def __init__(self, value: int) -> None:
        super().__init__("Cannot place this many warships")
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

    def __init__(self, size: int, num_warships: int) -> None:
        if (size < 0):
            raise NegativeValueError(size)
        else:
            self.__size = size
        if (num_warships < 0):
            raise NegativeValueError(num_warships)
        elif num_warships > self.__size:
            raise InvalidWarshipCountError(num_warships)
        else:
            self.__num_warships = num_warships
        self.__locations_warships = []
        self.__warships = []
        self.__hit = []

    @property
    def warships(self):
        warships_str = ""
        for warship in self.__warships:
            warships_str += f"{str(warship)} "
        return warships_str

    def is_location_available(self, x, y):
        return (x, y) not in self.__locations_warships

    def get_available_locations_horizontal(self, warship_size):
        locations = []
        for x in range(self.__size):
            for y in range(self.__size - warship_size + 1):
                locations_inner = []
                for size in range(warship_size):
                    if self.is_location_available(x, y+size):
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
                    if self.is_location_available(x+size, y):
                        locations_inner.append((x+size, y))
                if (len(locations_inner) == warship_size):
                    locations.append(locations_inner)
        return locations

    def draw_location(self, size_to_add: int, alignment: str):
        warship_size = size_to_add
        if alignment == "horizontal":
            available_locations = self.get_available_locations_horizontal(
                warship_size)
            return choice(available_locations)
        else:
            available_locations = self.get_available_locations_vertical(
                warship_size)
            return choice(available_locations)

    def is_possible_to_add(self, size, alignment):
        try:
            self.draw_location(size, alignment)
        except IndexError:
            return False
        return self.draw_location(size, alignment) is not None

    def draw_locations(self):
        warships_sizes = [size for size in range(1, self.__size+1)]
        warships_to_add = self.__num_warships
        warships_added = 0
        while warships_added < warships_to_add:
            to_add = choice(warships_sizes)
            alignment = choice(["horizontal", "vertical"])
            if self.is_possible_to_add(to_add, alignment):
                drawed_locations = self.draw_location(
                    to_add, alignment)

                self.add_warship(drawed_locations)
                warships_added += 1
            else:
                warships_sizes.remove(to_add)

    def add_warship(self, locations) -> None:
        self.__warships.append(
            Warship(locations, len(locations))
        )
        for x, y in locations:
            self.__locations_warships.append((x, y))

    def all_sunk(self) -> bool:
        for warship in self.__warships:
            if not warship.was_sunk():
                return False
        return True

    def hit(self, coordinates):
        x, y = coordinates
        if (x, y) not in self.__hit:
            self.__hit.append((x, y))
        else:
            return "You've already hit here before"
        return self.hit_warships(coordinates)

    def hit_warships(self, coordinates):
        return print_hit_warships_io(self.__warships, coordinates)

    def drawed_warships_str(self):
        return print_drawed_warships_io(self.__warships)

    def print_board(self) -> str:
        size = self.__size
        locations_warships = self.__locations_warships
        locations_hit = self.__hit
        return print_board_io(size, locations_warships, locations_hit)
