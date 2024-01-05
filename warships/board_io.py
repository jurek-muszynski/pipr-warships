from warship import Warship


def print_labels_horizontal_io(size: int) -> str:
    """
    Returns horizontal labels in the form of
    A B C D ..., depending on the board's size.

    :param size: board's size
    :type size: int
    """
    labels_horizontal = [chr(num+65) for num in range(0, size)]
    labels_horizontal_as_str = "   "
    for letter in labels_horizontal:
        labels_horizontal_as_str += f"{letter:^3}"
    return labels_horizontal_as_str


def print_board_io(size: int, locations_warships: list[tuple[int, int]],
                   locations_hit: list[tuple[int, int]], show_warships: bool) -> str:
    """
    Returns the board's string representation.\n
    [#] for hits missed,\n
    [o] for warships,\n
    [x] for warships hit,\n
    [ ] for empty locations or hidden warships

    :param size: board's size
    :type size: int

    :param locations_warships: list of warships' locations
    :type locations_warships: list[tuple[int,int]]

    :param locations_hit: list of locations hit at
    :type locations_hit: list[tuple[int,int]]

    :param show_warships: indicates whether warships should be visible
    :type show_warships: bool
    """
    board_str = print_labels_horizontal_io(size)
    board_str += "\n"
    for index in range(size):
        board_str += f"{index:<2} "
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

    :param warships: list of warships
    :type warships: list[Warship]
    """
    warships_sizes = [
        warship.size for warship in warships if not warship.was_sunk()]
    warships_sizes_dict = {size: warships_sizes.count(
        size) for size in warships_sizes}
    warship_str = ""
    for size in warships_sizes_dict:
        warship_str += f"{size} mast warship: x{warships_sizes_dict[size]}\n"
    return warship_str


def print_hit_warships_io(warships: list[Warship],
                          locations: list[tuple[int, int]]) -> tuple[bool, bool, int]:
    """
    Prints an appropriate message depending on the
    result of the hit\n
    Returns a tuple indicating the hit's result
    (was_hit, was_sunk, hit_warship_size)

    :param warships: list of warships
    :type warships: list[Warship]

    :param locations: list of locations that were sucessfully hit
    :type locations: list[tuple[int,int]]
    """
    for warship in warships:
        if warship.was_hit(locations):
            if warship.was_sunk():
                print(f"{str(warship)} sunk")
                return (True, True, warship.size)
            print(f"{str(warship)} hit")
            return (True, False, warship.size)
    print("Miss")
    return (False, False, 0)
