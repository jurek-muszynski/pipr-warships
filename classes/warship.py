
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


class Warship():
    """
    Warship class. Represents a single warship on the board,
    consisting of one, two or three blocks

    :param blocks: Represents the lists of blocks
    :type blocks: list[int]

    :param size: warship's size.
    :type size: int

    :param hits: warship's hit count
    :type hits: int
    """

    def __init__(self, blocks: list[int], size: int) -> None:
        self.__size = size
        self.__hits = 0
        if self.evaluate_blocks(blocks):
            self.__blocks = blocks

    @property
    def blocks(self):
        return self.__blocks

    @property
    def size(self) -> int:
        return self.__size

    @property
    def hits(self) -> int:
        return self.__hits

    def evaluate_blocks(self, blocks) -> bool:
        size = self.__size
        correct_blocks = []
        for x, y in blocks:
            if int(x) >= size or int(x) < 0:
                raise XCoordinateOutOfRangeError(x)
            if int(y) >= size or int(y) < 0:
                raise YCoordinateOutOfRangeError(y)
            else:
                correct_blocks.append((x, y))
        return correct_blocks == blocks

    def __str__(self) -> str:
        return f"{len(self.__blocks)} mast warship"

    def was_hit(self, coordinates) -> bool:
        if coordinates in self.__blocks:
            self.__hits += 1
            return True
        return False

    def was_sunk(self) -> bool:
        return self.__hits == self.__size
