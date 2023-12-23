from warship import Warship
from board_io import print_board_io, print_warships_io, print_hit_warships_io
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
        self.__warships = []
        self.__hit = []

    @property
    def warships(self):
        warships_str = ""
        for warship in self.__warships:
            warships_str += f"{str(warship)} "
        return warships_str

    @property
    def size(self) -> int:
        return self.__size

    def _is_location_available(self, x, y):
        for warship in self.__warships:
            for x_warship, y_warship in warship.blocks:
                if x == x_warship and y == y_warship:
                    return False
        return True

    def get_available_locations_horizontal(self, warship_size):
        locations = []
        for x in range(self.__size):
            for y in range(self.__size - warship_size + 1):
                locations_inner = []
                for size in range(warship_size):
                    if self._is_location_available(x, y+size):
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
                    if self._is_location_available(x+size, y):
                        locations_inner.append((x+size, y))
                if (len(locations_inner) == warship_size):
                    locations.append(locations_inner)
        return locations

    def draw_location(self, size_to_add: int):
        warship_size = size_to_add
        available_locations_h = self.get_available_locations_horizontal(
            warship_size)
        available_locations_v = self.get_available_locations_vertical(
            warship_size)
        available_locations = available_locations_v + available_locations_h
        return choice(available_locations)

    def draw_locations(self):
        warships_sizes = [size for size in range(
            self.__size if self.__size < 5 else 5, 0, -1)]
        warships_to_add = self.__num_warships
        warships_added = 0
        while warships_added < warships_to_add:
            to_add = warships_sizes[warships_added]
            drawed_locations = self.draw_location(
                to_add)
            self.add_warship(drawed_locations)
            warships_added += 1

    def add_warship(self, locations) -> None:
        warship_to_add = Warship(locations)
        self.__warships.append(
            warship_to_add
        )

    def warship_types(self) -> dict[int]:
        warships_sizes = [
            warship.size for warship in
            self.__warships if not warship.was_sunk()]
        warships_sizes_dict = {size: warships_sizes.count(
            size) for size in warships_sizes}
        return warships_sizes_dict

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
            print("You've already hit here before")
            return (False, False, 0)
        return print_hit_warships_io(self.__warships, coordinates)

    def hit_warships(self, coordinates):
        return print_hit_warships_io(self.__warships, coordinates)

    def warships_str(self):
        return print_warships_io(self.__warships)

    def print_board(self, show_warships: bool = False) -> str:
        size = self.__size
        locations_warships = []
        for warship in self.__warships:
            for (x, y) in warship.blocks:
                locations_warships.append((x, y))
        locations_hit = self.__hit
        return print_board_io(size, locations_warships,
                              locations_hit, show_warships)
