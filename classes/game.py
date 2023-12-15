from board import Board
from time import sleep


def modify_hit_input(hit_input):
    x = ord(hit_input[0])-65
    y = int(hit_input[1])
    return x, y


def main():
    print("Welcome to warships")
    board_size = input("Enter the size of your board > ")
    warships = input("Enter how many warships would you like > ")
    bd = Board(int(board_size), int(warships))
    bd.draw_locations()
    while True:
        print(bd.drawed_warships_str())
        print(bd.print_board())
        hit = modify_hit_input(input("Where would you like to hit > "))
        print(bd.hit(hit))
        sleep(0.5)
        if (bd.all_sunk()):
            print("All warships had been sunk")
            sleep(0.5)
            break


if __name__ == "__main__":
    main()
