from os import name
from pick import pick


def pick_location(options: list[list[tuple[int, int]]], size: int) -> int:
    """
    Lets the user choose locations for their assigned warships.\n
    Depending on the OS the user has to either:\n
    - enter the index of the chosen placement option manually (Windows)
    - use their arrow keys to choose the placement option (Linux)

    :param options: possible options for placing warships of a specified size
    :type options: list[list[tuple[int,int]]]

    :param size: size of a warship that has to be placed
    :type size: int
    """
    if name == "nt":
        print(f"Place your {size} mast warship\n")
        for count, locations in enumerate(options):
            print(f"{count:>3}: {locations}")
        print("\n")
        while True:
            choice = input(f"Enter your choice (0-{count}): ")
            if choice in [f"{num}" for num in range(count+1)]:
                return int(choice)
            else:
                print(
                    f"Invalid choice. Enter a number between 1 and {count}\n")
    else:
        title = f"Place your {size} mast warship"
        option, index = pick(
            options, title, indicator="->", default_index=0)
        return index
