from random import randint
from pick import pick
from board import Board
from time import sleep
from os import system


class ForbiddenInputError(Exception):
    pass


class Player():

    def __init__(self, board) -> None:
        self.__board = board
        self.__board_size = self.__board.size
        self.__warship_types = {
            size: 1 for size in range(board.size if
                                      board.size < 5 else 5, 0, -1)}

    @property
    def board_size(self) -> int:
        return self.__board_size

    @property
    def board(self) -> Board:
        return self.__board

    def hit(self, hit_input: str):
        x = str.title(hit_input[0])
        x = ord(x)-65
        y = int(hit_input[1])
        if x < 0 or x >= self.__board_size or y < 0 or y >= self.__board_size:
            raise ForbiddenInputError()
        return x, y

    def _format_locations(self, locations):
        formatted = []
        for location in locations:
            formatted_inner = []
            for location_inner in location:
                x, y = location_inner
                formatted_inner.append(chr(x+65) + str(y))
            formatted.append(formatted_inner)

        return formatted

    def place_warships(self):
        sleep(1)
        for size in self.__warship_types:
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
                system("clear")


class Ai(Player):

    def __init__(self, board, warship_types) -> None:
        super().__init__(board)
        self.__warship_types = warship_types
        self.__hit = []
        self.__last_hit_success = False
        self.__successfull_hit = []

    @property
    def warship_types(self) -> dict[int]:
        return self.__warship_types

    def choose_coordinates(self):
        x = randint(0, self.board_size-1)
        y = randint(0, self.board_size-1)
        return x, y

    def set_last_hit_success(self, success: bool):
        self.__last_hit_success = success
        if success:
            self.__successfull_hit.append(self.__hit[-1])

    def hit(self):
        if self.__last_hit_success:
            pass
        else:
            x, y = self.choose_coordinates()
            while (x, y) in self.__hit:
                x, y = self.choose_coordinates()
            self.__hit.append((x, y))
            return x, y
