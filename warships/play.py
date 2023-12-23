from game import Game
from time import sleep
from os import system


def menu():
    title = "Welcome to Warships with AI"
    print(":" * 29)
    print(f"{title:^29}")
    print(":" * 29)
    print("1. Start Game")
    print("2. Instructions")
    print("3. Exit")


def start():
    print("\nLet the game begin!")
    sleep(1)
    system("clear")
    board_size = input("Enter the size of your board: ")
    game = Game(int(board_size))
    game.play()


def instructions():
    print("Instructions: ")


def main():
    while True:
        menu()
        choice = input("\nEnter your choice (1-3): ")
        match(choice):
            case "1":
                start()
            case "2":
                instructions()
            case "3":
                sleep(1)
                print("Thanks for playing! See you soon :)")
                sleep(1)
                system("clear")
                break
            case _:
                print("Invalid choice. Enter a number between 1 and 3\n")


if __name__ == "__main__":
    main()
