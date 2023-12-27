from warship import Warship


def print_legend_horizontal_io(size: int) -> str:
    """
    Returns horizontal board's legend in the form of
    A B C D ..., depending on its size
    """
    legend_horizontal = [chr(num+65) for num in range(0, size)]
    legend_horizontal_as_str = "  "
    for letter in legend_horizontal:
        legend_horizontal_as_str += f"{letter:^3}"
    return legend_horizontal_as_str


def print_board_io(size: int, locations_warships: list[tuple[int]], locations_hit: list[tuple[int]], show_warships: bool) -> str:
    """
    Returns the board's string representation.
    [#] for hits missed,
    [o] for warships,
    [x] for warships hit,
    [ ] for empty locations or hidden warships
    """
    board_str = print_legend_horizontal_io(size)
    board_str += "\n"
    for index in range(size):
        board_str += f"{index} "
        for index_inner in range(size):
            if (index_inner, index) not in locations_warships:
                if (index_inner, index) not in locations_hit:
                    board_str += "[ ]"
                else:
                    board_str += "[#]"
            elif (index_inner, index) in locations_hit:
                board_str += "[x]"
            else:
                if show_warships:
                    board_str += "[o]"
                else:
                    board_str += "[ ]"
        board_str += "\n"
    return board_str


def print_warships_io(warships: list[Warship]) -> str:
    """
    Returns a string representation of all warships and
    the number of their type's occurances on the board
    e.g. 1 mast warship: x1
    """
    warships_sizes = [
        warship.size for warship in warships if not warship.was_sunk()]
    warships_sizes_dict = {size: warships_sizes.count(
        size) for size in warships_sizes}
    warship_str = ""
    for size in warships_sizes_dict:
        warship_str += f"{size} mast warship: x{warships_sizes_dict[size]}\n"
    return warship_str


def print_hit_warships_io(warships: list[Warship], coordinates: list[tuple[int]]) -> tuple[bool, bool, int]:
    """
    Prints appropriate message depending on the
    result of the hit
    Returns a tuple of 3 values describing the hit's result
    (was_hit, was_sunk, hit_warship_size)
    """
    for warship in warships:
        if warship.was_hit(coordinates):
            if warship.was_sunk():
                print(f"{str(warship)} sunk")
                return (True, True, warship.size)
            print(f"{str(warship)} hit")
            return (True, False, warship.size)
    print("Miss")
    return (False, False, 0)
