from random import choice
from pick import pick
from board import Board
from time import sleep
from os import system
from consts import MAX_NUM_OF_WARSHIPS
from system import clear


class Player():

    def __init__(self, board) -> None:
        self.__board = board
        self.__warship_types = {
            size: 1 for size in range(board.size if
                                      board.size < MAX_NUM_OF_WARSHIPS
                                      else MAX_NUM_OF_WARSHIPS, 0, -1)}

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

    def __init__(self, board) -> None:
        super().__init__(board)
        self.__hit = []
        self.__success_hit = []
        self.__warships = {size: [] for size in self.warship_types.keys()}
        self.__next_hit = 0

    def remove_duplicates(self, locations):
        return [coors for coors in locations if coors not in self.__hit]

    def draw_coordinates(self):
        all_locations = []
        warships_coordinates = sum(self.__warships.values(), [])
        for x in range(self.board.size):
            for y in range(self.board.size):
                if (x, y) not in warships_coordinates:
                    all_locations.append((x, y))
        return choice(self.remove_duplicates(all_locations))

    def get_possible_locations_horizontal(self, warship_size):
        locations = []
        for x in range(self.board.size):
            for y in range(self.board.size - warship_size + 1):
                locations_inner = []
                for size in range(warship_size):
                    locations_inner.append((x, y+size))
                if (len(locations_inner) == warship_size):
                    locations.append(locations_inner)
        return locations

    def get_possible_locations_vertical(self, warship_size):
        locations = []
        for x in range(self.board.size - warship_size + 1):
            for y in range(self.board.size):
                locations_inner = []
                for size in range(warship_size):
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

    def get_warship_key(self, coors):
        for key, values in self.__warships.items():
            if coors in values:
                return key

    def set_last_hit(self, last_hit):
        was_hit, was_sunk, size = last_hit
        if not was_hit:
            if self.__success_hit == []:
                self.__next_hit = self.draw_coordinates()
            else:
                key = self.get_warship_key(self.__success_hit[-1])
                possible_locations = self.get_next_possible_location(
                    key, self.__warships[key])
                possible_locations_cleaned_up = self.remove_duplicates(
                    possible_locations)
                # print(self.__success_hit[-1],
                #       possible_locations_cleaned_up, "not hit")
                self.__next_hit = choice(possible_locations_cleaned_up)

            return
        else:
            self.__success_hit.append(self.__hit[-1])
            self.__warships[size].append(self.__hit[-1])
            if was_sunk:
                for coors in self.__warships[size]:
                    self.__success_hit.remove(coors)
                if len(self.__success_hit) == 0:
                    self.__next_hit = 0
                    return
                else:
                    key = self.get_warship_key(self.__success_hit[-1])
                    possible_locations = self.get_next_possible_location(
                        key, self.__warships[key])
                    possible_locations_cleaned_up = self.remove_duplicates(
                        possible_locations)
                    # print(
                    #     self.__success_hit[-1], possible_locations_cleaned_up, "sunk")
                    self.__next_hit = choice(possible_locations_cleaned_up)
                    return
            possible_locations = self.get_next_possible_location(
                size, self.__warships[size])
            possible_locations_cleaned_up = self.remove_duplicates(
                possible_locations)
            # print(self.__success_hit[-1],
            #       possible_locations_cleaned_up, "hit")
            self.__next_hit = choice(possible_locations_cleaned_up)
            return

    def smart_hit(self):
        if len(self.__hit) == 0 or self.__next_hit == 0:
            coordinates = self.draw_coordinates()
        else:
            coordinates = self.__next_hit
        self.__hit.append(coordinates)
        return coordinates
