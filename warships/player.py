from random import choice
from pick import pick
from board import Board
from time import sleep
from consts import MAX_NUM_OF_WARSHIPS
from system import clear


class Player():
    """
    Player class. Contains attributes:

    :param board: a board with player's warships
    :type board: Board

    :param warship_types: types of warships with their count on the board
    :type wraship_types: dict[int, int]
    """

    def __init__(self, board: Board) -> None:
        """
        Creates an instance of the Player class
        When initialized, board is empty

        :param board: player's board
        :type board: Board
        """
        self.__board = board
        self.__warship_types = {
            size: 1 for size in range(board.size if
                                      board.size < MAX_NUM_OF_WARSHIPS
                                      else MAX_NUM_OF_WARSHIPS, 0, -1)}

    @property
    def board(self) -> Board:
        return self.__board

    @property
    def warship_types(self) -> dict[int, int]:
        return self.__warship_types

    def hit(self, hit_input: str) -> tuple[int, int]:
        """
        Parses a hit entered by the user to a tuple of integers

        :param hit_input: hit entered by the user e.g. A0 -> (0,0)
        :type hit: str
        """
        x = str.title(hit_input[0])
        x = ord(x)-65
        y = int(hit_input[1])
        return x, y

    def _format_locations(self,
                          locations: list[list[tuple[int, int]]]) -> list[list[str]]:
        """
        Parses a list of locations so that they could be presented
        in the same format as the user gets to enter them, e.g (0,0) -> A0

        :param locations: a list of locations
        :type loations: list[list[tuple[int]]]
        """
        formatted = []
        for location in locations:
            formatted_inner = []
            for location_inner in location:
                x, y = location_inner
                formatted_inner.append(chr(x+65) + str(y))
            formatted.append(formatted_inner)

        return formatted

    def place_warships(self) -> None:
        """
        Allows the user to choose their wanted locations for
        all assigned warships,
        The order is descending, biggest ships are to be chosen first
        """
        sleep(1)
        for size in self.__warship_types:
            clear()
            to_add = self.__warship_types.get(size)
            added = 0
            while added < to_add:
                title = f"Place your {size} mast warship"
                available_locations = (self.board.get_available_locations_horizontal(
                    size)) + (self.board.get_available_locations_vertical(size))
                unique_available_locations = []
                [unique_available_locations.append(
                    location) for location in available_locations if
                    location not in unique_available_locations]
                options = self._format_locations(unique_available_locations)
                option, index = pick(
                    options, title, indicator="->", default_index=0)
                self.board.add_warship(
                    unique_available_locations[index]
                )
                added += 1
                print(self.board.print_board(True))
                sleep(1)
        clear()


class Ai(Player):
    """
    Ai class, derives from Player class. Contains attributes:

    :param board: a board with ai's warships
    :type board: Board

    :param hit: all hits made by the ai
    :type hit: list[tuple[int, int]]

    :param success_hit: all successful hits made by the ai
    :type success_hit: list[tuple[int, int]]

    :param warships_hit: successful hit locations assigned to the sizes of those hit warships
    :type warships_hit: dict[int, list[tuple[int,int]]]

    :param next_hit: hit to be made next by the ai
    :type next_hit: tuple[int,int]
    """

    def __init__(self, board: Board) -> None:
        """
        Creates an instance of the Ai class.
        When initialized, hit, success_hit, warships_hit.values() are empty &
        next_hit is set to 0

        :param board: a board with ai's warships
        :type board: Board
        """
        super().__init__(board)
        self.__hit = []
        self.__success_hit = []
        self.__warships_hit = {size: [] for size in self.warship_types.keys()}
        self.__next_hit = 0

    def remove_hit_before(self,
                          locations: list[tuple[int, int]]) -> list[tuple[int, int]]:
        """
        Returns a list of locations without those already hit at before

        :param locations: list of locations(coordinates)
        :type locations: list[tuple[int,int]]

        """
        return [coors for coors in locations if coors not in self.__hit]

    def draw_coordinates(self) -> tuple[int, int]:
        """
        Returns a randomly chosen pair of available coordinates on the board
        """
        all_locations = []
        warships_coordinates = sum(self.__warships_hit.values(), [])
        for x in range(self.board.size):
            for y in range(self.board.size):
                if (x, y) not in warships_coordinates:
                    all_locations.append((x, y))
        return choice(self.remove_hit_before(all_locations))

    def get_possible_locations_horizontal(self, warship_size: int) -> list[tuple[int, int]]:
        """
        Returns a list of all possible horizontal locations for warships
        of a specified size

        :param warship_size: size of a warship
        :type warship_size: int
        """
        locations = []
        for x in range(self.board.size):
            for y in range(self.board.size - warship_size + 1):
                locations_inner = []
                for size in range(warship_size):
                    locations_inner.append((x, y+size))
                if (len(locations_inner) == warship_size):
                    locations.append(locations_inner)
        return locations

    def get_possible_locations_vertical(self, warship_size: int) -> list[tuple[int, int]]:
        """
        Returns a list of all possible vertical locations for warships
        of a specified size

        :param warship_size: size of a warship
        :type warship_size: int
        """
        locations = []
        for x in range(self.board.size - warship_size + 1):
            for y in range(self.board.size):
                locations_inner = []
                for size in range(warship_size):
                    locations_inner.append((x+size, y))
                if (len(locations_inner) == warship_size):
                    locations.append(locations_inner)
        return locations

    def flatten_valid_locations(self, locations: list[list[tuple[int, int]]],
                                hits: list[tuple[int, int]]):
        """
        Returns a flattened list of all locations, without
        those already hit at, so that there is no nesting inside

        :param locations: nested list of locations
        :type locations: list[list[tuple[int,int]]]

        :param hits: list of locations already hit at
        :type hits: list[tuple[int,int]]
        """
        flattened_locations = []
        for locations_inner in locations:
            flattened_locations.append([
                coors for coors in locations_inner if coors not in hits
            ])
        return sum(flattened_locations, [])

    def get_next_possible_locations(self, size: int,
                                    hits: list[tuple[int, int]]) -> list[tuple[int, int]]:
        """
        Returns a list of next possible locations based on
        what hits were made by the ai before

        :param size: hit warship's size
        :type size: int

        :param hits: list of hit locations of a particular hit warship
        :type hits: list[tuple[int, ints]]
        """
        possible_locations = self.get_possible_locations_horizontal(size) + \
            self.get_possible_locations_vertical(size)
        valid_locations = []
        for locations in possible_locations:
            valid = True
            for hit in hits:
                if hit not in locations:
                    valid = False
            for hit in self.__hit:
                if hit not in hits and hit in locations:
                    valid = False
            if valid:
                valid_locations.append(locations)
        return self.flatten_valid_locations(valid_locations, hits)

    def get_warship_key(self, location: tuple[int, int]) -> int:
        """
        Returns the size of a warship, which specified
        location has been hit

        :param location: hit coordinates of a warship
        :type location: tuple[int,int]
        """
        for key, values in self.__warships_hit.items():
            if location in values:
                return key

    def set_next_hit_with_key(self, key: int) -> tuple[int, int]:
        """
        Returns a randomly chosen next possible location
        of a warship

        :param key: size of a warship, hit before
        :type key: int
        """
        possible_locations = self.get_next_possible_locations(
            key, self.__warships_hit[key])
        possible_locations_cleaned_up = self.remove_hit_before(
            possible_locations)
        # print(self.__success_hit[-1],
        #       possible_locations_cleaned_up)
        return choice(possible_locations_cleaned_up)

    def set_next_hit(self, last_hit: tuple[bool, bool, int]) -> None:
        """
        Sets the next hit based on the result of the last hit.

        :param last_hit: result of the last hit, contains following:
        (was_hit, was_sunk, hit_warship_size)
        :type last_hit: tuple[bool, bool, int]

        If last_hit wasn't successful it either:\n
        -sets next hit randomly, if there were no successful hits before\n
        -sets next hit based on the last successful hit\n

        If last_hit was successful and sank a warship, it either:\n
        -sets next hit randomly, if there were no successful hits before\n
        -sets next hit based on the last successful hit\n

        If last_hit was successful but didn't sink a warship, it:\n
        -sets next hit based on the last successful hit\n
        """
        was_hit, was_sunk, size = last_hit
        if not was_hit:
            if self.__success_hit == []:
                self.__next_hit = self.draw_coordinates()
            else:
                self.__next_hit = self.set_next_hit_with_key(
                    self.get_warship_key(self.__success_hit[-1]))
            return
        else:
            self.__success_hit.append(self.__hit[-1])
            self.__warships_hit[size].append(self.__hit[-1])
            if was_sunk:
                for coors in self.__warships_hit[size]:
                    self.__success_hit.remove(coors)
                if len(self.__success_hit) == 0:
                    self.__next_hit = 0
                    return
                else:
                    self.__next_hit = self.set_next_hit_with_key(
                        self.get_warship_key(self.__success_hit[-1]))
                    return
            self.__next_hit = self.set_next_hit_with_key(size)
            return

    def smart_hit(self) -> tuple[int, int]:
        """
        Returns a hit based on the next_hit parameter's value.

        If next_hit is 0 and there weren't any hits before:\n
        -the hit will by drawn randomly\n

        Otherwise returns the next_hit parameter's value
        """
        if len(self.__hit) == 0 or self.__next_hit == 0:
            coordinates = self.draw_coordinates()
        else:
            coordinates = self.__next_hit
        self.__hit.append(coordinates)
        return coordinates
