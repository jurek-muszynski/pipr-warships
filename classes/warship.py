
class XCoordinateOutOfRangeError(Exception):
    """
    XCoordinateOutOfRangeError Exception.
    Raised when an x coordinate is not within the board's range

    :param invalid_x_coordinate: Represents an x coordinate out of range
    :type invalid_x_coordinate: str
    """

    def __init__(self, coordinate: str) -> None:
        super().__init__("x Coordinate must be within the board's range")
        self.__invalid_x_coordinate = coordinate


class YCoordinateOutOfRangeError(Exception):
    """
    YCoordinateOutOfRangeError Exception.
    Raised when a y coordinate is not within the board's range

    :param invalid_y_coordinate: Represents a y coordinate out of range
    :type invalid_y_coordinate: int
    """

    def __init__(self, coordinate: int) -> None:
        super().__init__("y Coordinate must be within the board's range")
        self.__invalid_y_coordinate = coordinate


class Block():
    """
    Block class. Represents a single point on the 2 dimensional board

    :param x: x coordinate on the board, represented as a letter (A-...)
    :type x: str

    :param y: y coordinate on the board, represented as an integer (0-...)
    :type y: int
    """

    def __init__(self, x: str, y: int) -> None:
        self.__x = x
        self.__y = y

    @property
    def x(self) -> str:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y


class Warship():
    """
    Warship class. Represents a single warship on the board,
    consisting of one, two or three blocks

    :param blocks: Represents the lists of blocks

    :param size: warship's size.
    :type size: int
    """

    def __init__(self, blocks: list[Block]) -> None:
        self.__blocks = blocks
        self.__size = len(blocks)

    @property
    def blocks(self) -> list[Block]:
        return self.__blocks

    @property
    def size(self) -> int:
        return self.__size
