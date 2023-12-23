def print_legend_horizontal_io(size):
    legend_horizontal = [chr(num+65) for num in range(0, size)]
    legend_horizontal_as_str = "  "
    for letter in legend_horizontal:
        legend_horizontal_as_str += f"{letter:^3}"
    return legend_horizontal_as_str


def print_board_io(size, locations_warships, locations_hit, show_warships):
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


def print_warships_io(warships):
    warships_sizes = [
        warship.size for warship in warships if not warship.was_sunk()]
    warships_sizes_dict = {size: warships_sizes.count(
        size) for size in warships_sizes}
    warship_str = "Warships to sink:\n"
    for size in warships_sizes_dict:
        warship_str += f"{size} mast warship: x{warships_sizes_dict[size]}\n"
    return warship_str


def print_hit_warships_io(warships, coordinates):
    for warship in warships:
        if warship.was_hit(coordinates):
            if warship.was_sunk():
                return f"You've sunk a {str(warship)}"
            return f"You've hit a {str(warship)}"
    return "Miss"
