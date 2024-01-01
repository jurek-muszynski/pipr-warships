from game import Game
from time import sleep
from system import clear
from os import name


def menu() -> None:
    """
    Prints out the main menu of the game, a user
    can choose to either:\n
    1 - Start the game\n
    2 - See the instructions\n
    3 - Exit the game
    """
    title = "Welcome to Warships with AI"
    print(":" * 29)
    print(f"{title:^29}")
    print(":" * 29)
    print("1. Start Game")
    print("2. Instructions")
    print("3. Exit")


def start() -> None:
    """
    Initializes the Game object & enters the
    game's main loop

    Raises ValueError if passed board size is invalid
    """
    print("\nLet the game begin!")
    sleep(1)
    clear()
    while True:
        try:
            board_size = input("Enter the size of your board: ")
            game = Game(board_size)
            break
        except ValueError:
            print("Invalid board size")
    game.play()


def instructions() -> None:
    """
    Prints out the game's instructions
    """
    clear()
    print("Instructions: ")
    sleep(1)
    print("\nBOARD PREP\n")
    print("1 > Choose the size of your board e.g. (2)")
    if name == "nt":
        print("2 > Chose where to place your warships")
    else:
        print(
            "2 > Use the arrow keys to place your warships according to your liking")
    sleep(1)
    print("\nGAME ON\n")
    print("1 > Take turns with the AI on hitting the opponent's ships")
    print(
        "2 > Enter your hits in the following format e.g. A0 (column A row 0)")
    print(
        "3 > x will be displayed in the chosen coordinates, if the hit was successful")
    print(
        "4 > # will be displayed in the chosen coordinates, if the hit a miss\n")
    sleep(1)
    input("Press Enter to continue: ")
    clear()


def main() -> None:
    while True:
        menu()
        choice = input("\nEnter your choice (1-3): ")
        match(choice):
            case "1":
                start()
            case "2":
                sleep(1)
                instructions()
            case "3":
                sleep(1)
                print("Thanks for playing! See you soon :)")
                sleep(1)
                clear()
                break
            case _:
                print("Invalid choice. Enter a number between 1 and 3\n")


if __name__ == "__main__":
    main()
