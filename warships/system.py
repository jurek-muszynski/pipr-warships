from os import system, name


def clear() -> None:
    """
    Clears out the console window
    """
    if name == "nt":
        system("cls")
    else:
        system("clear")
