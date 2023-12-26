from warship import Warship
from board_io import print_board_io, print_warships_io, print_hit_warships_io
from random import choice
from consts import MAX_NUM_OF_WARSHIPS


class InvalidWarshipCountError(Exception):
    """
    InvalidWarshipCountError Exception.
    Raised when this many warships cannot be placed on the board

    :param value: passed value
    :type value: int

    """

    def __init__(self, value: int) -> None:
        super().__init__("Cannot place this many warships")
        self.value = value


class InvalidWarshipError(Exception):
    """
    InvalidWarshipError Exception.
    Raised when a warship cannot be placed on the board

    :param warship: invalid warship
    :type warship: Warship
    """

    def __init__(self, invalid: Warship) -> None:
        super().__init__("Cannot place this warship")
        self.invalid = invalid


class CoordinatesOutOfRangeError(Exception):
    """
   CoordinatesOutOfRangeError Exception.
   Raised when passed coordinates aren't within the board

   :param coordinates: invalid coordinates
   :type coordinates: tuple[int]
   """

    def __init__(self, coordinates: tuple[int]) -> None:
        super().__init__("Coordinates out of range")
        self.cordinates = coordinates


class Board():
    """
    Board class. Contains attributes:

    :param size: number of either rows/columns, as the board is a square
    :type size: int

    :param num_warships: number of warships situated on the board, <= size
    :type num_warships: int

    :param warships: warship objects situated on the board
    :type warships: list[Warship]

    :param hit: hit coordinates
    :type hit: list[tuple[int]]
    """

    def __init__(self, size: int, num_warships: int) -> None:
        """
        Creates an instance of the board class.
        Raises ValueError if size is less/equal 0.
        Raises ValueError if number of warships is less/equal 0.
        Raises InvalidWarshipCountError if number of warships greater than size.
        Initially 'warships' and 'hit' lists are empty
        """
        if (size <= 0):
            raise ValueError(size)
        else:
            self.__size = size
        if (num_warships <= 0):
            raise ValueError(num_warships)
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

    def all_locations(self) -> list[tuple[int]]:
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
        e.g. 1 mast warship 2 mast warship
        """
        warships_str = ""
        for warship in self.__warships:
            warships_str += f"{str(warship)} "
        return warships_str

    def evaluate_warship(self, warship_to_add: Warship) -> None:
        """
        Checks if a warship can be added to the board.
        Raises InvalidWarshipError if warship.size > size
        Raises InvalidWarshipError if any of its blocks' coordinates
        are out of board's range
        """
        if warship_to_add.size > self.__size:
            raise InvalidWarshipError(warship_to_add)
        for x, y in warship_to_add.blocks:
            if x >= self.__size or y >= self.__size:
                raise InvalidWarshipError(warship_to_add)

    def _is_location_available(self, x: int, y: int) -> bool:
        """
        Checks if a specified pair of coordinates is available on the board
        (no warships' blocks there)
        """
        for warship in self.__warships:
            for x_warship, y_warship in warship.blocks:
                if x == x_warship and y == y_warship:
                    return False
        return True

    def get_available_locations_horizontal(self, warship_size: int) -> list[list[tuple[int]]]:
        """
        Returns a list of all possible horizontal locations of warships
        of a specified size
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

    def get_available_locations_vertical(self, warship_size: int) -> list[list[tuple[int]]]:
        """
        Returns a list of all possible vertical locations of warships
        of a specified size
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

    def draw_location(self, warship_size: int) -> list[tuple[int]]:
        """
        Randomly chooses one of all possible locations
        for a warship of a specified size
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

    def add_warship(self, locations: list[tuple[int]]) -> None:
        """
        Adds a warship of specified coordinates to the board
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

    def hit(self, coordinates: tuple[int]) -> tuple[bool, bool, int]:
        """
        Hits specified coordinates.
        Prints appropriate message depending on the
        result of that shot
        Returns a tuple of 3 values describing that shot's result
        (was_hit, was_sunk, hit_warship_size)
        """
        x, y = coordinates
        if (x, y) not in self.all_locations():
            raise CoordinatesOutOfRangeError((x, y))
        else:
            if (x, y) not in self.__hit:
                self.__hit.append((x, y))
            else:
                print("You've already hit here before")
                return (False, False, 0)
            return print_hit_warships_io(self.__warships, coordinates)

    def warships_str(self) -> str:
        """
        Returns a string representation of all warships and
        the number of their type's occurances on the board
        e.g. 1 mast warship: x1
        """
        return print_warships_io(self.__warships)

    def print_board(self, show_warships: bool = False) -> str:
        """
        Prints the board in the console window.
        If show_warships param is set to True, then it
        prints the locations of warships, otherwise
        they remain hidden
        """
        size = self.__size
        locations_warships = []
        for warship in self.__warships:
            for (x, y) in warship.blocks:
                locations_warships.append((x, y))
        locations_hit = self.__hit
        return print_board_io(size, locations_warships,
                              locations_hit, show_warships)
