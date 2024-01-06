from .warship import Warship
from utils.board_io import (print_board_io,
                            print_warships_io, print_hit_warships_io)
from random import choice
from utils.consts import MAX_NUM_OF_WARSHIPS, MAX_BOARD_SIZE


class InvalidWarshipCountError(Exception):
    """
    InvalidWarshipCountError Exception.\n
    Raised when that many warships cannot be placed on the board

    :param value: passed value
    :type value: int
    """

    def __init__(self, value: int) -> None:
        super().__init__("Cannot place that many warships")
        self.value = value


class InvalidWarshipError(Exception):
    """
    InvalidWarshipError Exception.\n
    Raised when a warship cannot be placed on the board

    :param warship: invalid warship
    :type warship: Warship
    """

    def __init__(self, invalid: Warship) -> None:
        super().__init__("Cannot place that warship")
        self.invalid = invalid


class CoordinatesOutOfRangeError(Exception):
    """
    CoordinatesOutOfRangeError Exception.\n
    Raised when passed coordinates aren't within the board

   :param coordinates: invalid coordinates
   :type coordinates: tuple[int,int]
   """

    def __init__(self, coordinates: tuple[int, int]) -> None:
        super().__init__("Coordinates out of range")
        self.cordinates = coordinates


class Board():
    """
    Board class. Contains attributes:

    :param size: number of either rows/columns
    :type size: int

    :param num_warships: number of warships situated on the board, <= size
    :type num_warships: int

    :param warships: warship objects situated on the board
    :type warships: list[Warship]

    :param hit: list of hit locations
    :type hit: list[tuple[int, int]]
    """

    def __init__(self, size: int, num_warships: int) -> None:
        """
        Creates an instance of the board class.\n
        Raises ValueError if size is less/equal 1.\n
        Raises ValueError if size is greater than MAX_BOARD_SIZE.\n
        Raises InvalidWarshipCountError if number of warships is less/equal 0\n
        Raises InvalidWarshipCountError if number of warships is greater
        than size.\n
        Initially 'warships' and 'hit' lists are empty.

        :param size: board's size
        :type size: int

        :param num_warships: number of warships on the board
        :type num_warships: int
        """
        if size <= 1 or size > MAX_BOARD_SIZE:
            raise ValueError(size)
        else:
            self.__size = size
        if (num_warships <= 0):
            raise InvalidWarshipCountError(num_warships)
        elif num_warships > self.__size:
            raise InvalidWarshipCountError(num_warships)
        else:
            self.__num_warships = num_warships
        self.__warships = []
        self.__hit = []

    @property
    def size(self) -> int:
        return self.__size

    @property
    def num_warships(self) -> int:
        return self.__num_warships

    def all_locations(self) -> list[tuple[int, int]]:
        """
        Returns a list of all possible coordinates on the board e.g. (x,y)
        """
        locations = []
        for x in range(self.__size):
            for y in range(self.__size):
                locations.append((x, y))
        return locations

    def warships(self) -> str:
        """
        Returns a string representation of all warships
        e.g. 1 mast warship 2 mast warship.
        """
        warships_str = ""
        for warship in self.__warships:
            warships_str += f"{str(warship)} "
        return warships_str

    def evaluate_warship(self, warship_to_add: Warship) -> None:
        """
        Checks if a warship can be added to the board.\n
        Raises InvalidWarshipError if warship.size > size\n
        Raises InvalidWarshipError if any of its blocks' coordinates
        are out of board's range.

        :param warship_to_add: warship to be added to the board
        :type warship_to_add: Warship
        """
        if warship_to_add.size > self.__size:
            raise InvalidWarshipError(warship_to_add)
        for x, y in warship_to_add.blocks:
            if x >= self.__size or y >= self.__size:
                raise InvalidWarshipError(warship_to_add)
            if not self._is_location_available(x, y):
                raise InvalidWarshipError(warship_to_add)

    def _is_location_available(self, x: int, y: int) -> bool:
        """
        Checks if a specified pair of coordinates is available on the board
        (no warships' blocks there)

        :param x: horizontal axis coordinate
        :type x: int

        :param y: vertical axis coordinate
        :type y: int
        """
        for warship in self.__warships:
            for x_warship, y_warship in warship.blocks:
                if x == x_warship and y == y_warship:
                    return False
        return True

    def get_available_locations_horizontal(self,
                                           warship_size: int) -> list[list[tuple[int, int]]]:
        """
        Returns a list of all possible horizontal locations for warships
        of a specified size

        :param warship_size: size of a warship
        :type warship_size: int
        """
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

    def get_available_locations_vertical(self,
                                         warship_size: int) -> list[list[tuple[int, int]]]:
        """
        Returns a list of all possible vertical locations for warships
        of a specified size

        :param warship_size: size of a warship
        :type warship_size: int
        """
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

    def draw_location(self, warship_size: int) -> list[tuple[int, int]]:
        """
        Randomly chooses one of all possible locations
        for a warship of a specified size

        :param warship_size: size of a warship
        :type warship_size: int
        """
        available_locations_h = self.get_available_locations_horizontal(
            warship_size)
        available_locations_v = self.get_available_locations_vertical(
            warship_size)
        available_locations = available_locations_v + available_locations_h
        return choice(available_locations)

    def draw_locations(self) -> None:
        """
        Randomly chooses locations for all warships
        to be added to the board
        """
        warships_sizes = [size for size in range(
            self.__size if self.__size < MAX_NUM_OF_WARSHIPS
            else MAX_NUM_OF_WARSHIPS, 0, -1)]
        warships_to_add = self.__num_warships
        warships_added = 0
        while warships_added < warships_to_add:
            to_add = warships_sizes[warships_added]
            drawed_locations = self.draw_location(
                to_add)
            self.add_warship(drawed_locations)
            warships_added += 1

    def add_warship(self, locations: list[tuple[int, int]]) -> None:
        """
        Adds a warship of specified blocks of coordinates to the board

        :param locations: blocks of coordinates that a warship is made of
        :type locations: list[tuple[int, int]]
        """
        warship_to_add = Warship(locations)
        self.evaluate_warship(warship_to_add)
        self.__warships.append(
            warship_to_add
        )

    def all_sunk(self) -> bool:
        """
        Checks if all warships had been sunk.
        (Returns false if the board is empty)
        """
        for warship in self.__warships:
            if not warship.was_sunk():
                return False
        return len(self.__warships) > 0

    def hit(self, coordinates: tuple[int, int]) -> tuple[bool, bool, int]:
        """
        Hits specified coordinates.\n
        Returns a tuple of 3 values describing the hit's result
        (was_hit, was_sunk, hit_warship_size)\n
        Raises CoordinatesOutOfRangeError if passed coordinates
        out of the board's bounds

        :param coordinates: coordinates of a location on the board
        :type coordinates: tuple[int, int]
        """
        x, y = coordinates
        if (x, y) not in self.all_locations():
            raise CoordinatesOutOfRangeError((x, y))
        else:
            if (x, y) not in self.__hit:
                self.__hit.append((x, y))
            else:
                print_hit_warships_io(False, False, 0)
                return (False, False, 0)
            for warship in self.__warships:
                if warship.was_hit(coordinates):
                    if warship.was_sunk():
                        print_hit_warships_io(True, True, warship)
                        return (True, True, warship.size)
                    print_hit_warships_io(True, False, warship)
                    return (True, False, warship.size)
            print_hit_warships_io(False, False)
            return (False, False, 0)

    def warships_str(self) -> str:
        """
        Returns a string representation of all warships with
        their respective types and the number of those specific
        warships left on the board\n
        e.g. 1 mast warship: x1
        """
        return print_warships_io(self.__warships)

    def print_board(self, show_warships: bool = False) -> str:
        """
        Prints the board in the console window.\n
        If show_warships param is True, then it
        shows the locations of warships, otherwise
        they remain hidden

        :param show_warships: determines the visibility of printed warships
        :type show_warships: bool
        """
        size = self.__size
        locations_warships = []
        for warship in self.__warships:
            for (x, y) in warship.blocks:
                locations_warships.append((x, y))
        locations_hit = self.__hit
        return print_board_io(size, locations_warships,
                              locations_hit, show_warships)
