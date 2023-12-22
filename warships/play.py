from game import Game


def main():
    print("Welcome to Warships")
    board_size = input("Enter the size of your board > ")
    # warships = input(
    #     f"Enter how many warships you would like [1-{board_size}] > ")
    game = Game(int(board_size))
    game.play()


if __name__ == "__main__":
    main()
