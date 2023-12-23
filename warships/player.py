from random import randint, choice
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

    @property
    def warship_types(self):
        return self.__warship_types

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

    def __init__(self, board) -> None:
        super().__init__(board)
        self.__hit = []
        self.__success_hit = []
        self.__warships = {size: [] for size in self.warship_types.keys()}
        self.__next_hit = 0

    def choose_coordinates(self):
        x = randint(0, self.board_size-1)
        y = randint(0, self.board_size-1)
        return x, y

    def _is_location_available(self, x, y):
        return (x, y) not in sum(self.__warships.values(), [])

    def get_possible_locations_horizontal(self, warship_size):
        locations = []
        for x in range(self.board_size):
            for y in range(self.board_size - warship_size + 1):
                locations_inner = []
                for size in range(warship_size):
                    # if self._is_location_available(x, y+size):
                    locations_inner.append((x, y+size))
                if (len(locations_inner) == warship_size):
                    locations.append(locations_inner)
        return locations

    def get_possible_locations_vertical(self, warship_size):
        locations = []
        for x in range(self.board_size - warship_size + 1):
            for y in range(self.board_size):
                locations_inner = []
                for size in range(warship_size):
                    # if self._is_location_available(x+size, y):
                    locations_inner.append((x+size, y))
                if (len(locations_inner) == warship_size):
                    locations.append(locations_inner)
        return locations

    def flatten_valid_locations(self, locations, hits):
        flattened_locations = []
        for locations_inner in locations:
            flattened_locations.append([
                coors for coors in locations_inner if coors not in hits
            ])
        return sum(flattened_locations, [])

    def get_next_possible_location(self, size, hits):
        possible_locations = self.get_possible_locations_horizontal(size) + \
            self.get_possible_locations_vertical(size)

        # return ([locations for locations in possible_locations if
        #          hit in locations])

        valid_locations = []

        for locations in possible_locations:
            valid = True
            for hit in hits:
                if hit not in locations:
                    valid = False
            if valid:
                valid_locations.append(locations)

        return self.flatten_valid_locations(valid_locations, hits)

    def set_last_hit(self, last_hit):
        # Unpacking last_hit parameters (was_hit, was_sunk, warship_size)
        # If not hit, then continue
        # If sunk, delete last successful hit
        # If hit & not sunk, ...
        was_hit, was_sunk, size = last_hit
        if not was_hit:
            self.__next_hit == self.choose_coordinates()
            return
        else:
            # print(self.__hit)
            self.__success_hit.append(self.__hit[-1])
            self.__warships[size].append(self.__hit[-1])
            if was_sunk:
                for coors in self.__warships[size]:
                    self.__success_hit.remove(coors)
                self.__warships.pop(size)
                return
            possible_locations = self.get_next_possible_location(
                size, self.__warships[size])
            self.__next_hit = choice(possible_locations)
            return

    def smart_hit(self):
        # if self.__last_hit_success:
        #     pass
        # else:
        if len(self.__hit) == 0 or self.__next_hit == 0:
            coordinates = self.choose_coordinates()
        else:
            coordinates = self.__next_hit
        self.__hit.append(coordinates)
        return coordinates


# ai = Ai(Board(2, 2))
# ai.__hit = [(0, 0)]
# print((ai.set_last_hit((True, False, 2))))
