class InvalidCoordinatesError(Exception):
    """
    InvalidCoordinates Exception.
    Raised when one of the coordinates is out of range
    """

    def __init__(self) -> None:
        super().__init__("Invalid coordinates")


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
        """
        Creates an instance of a warship.
        Raises InvalidCoordinatesError Exception if coordiantes are invalid
        """
        self.__size = size
        self.__hits = 0
        if self.evaluate_blocks(blocks):
            self.__blocks = blocks
        else:
            raise InvalidCoordinatesError()

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
        """
        Checks if all blocks passed in the arguments' list are correct
        """
        size = self.__size
        correct_blocks = [(int(x), int(y)) for x, y in blocks if
                          int(x) >= 0 and int(x) < size and
                          int(y) >= 0 and int(y) < size]
        return correct_blocks == blocks

    def __str__(self) -> str:
        """
        Returns a sample description of a warship:
        {n} mast warship
        """
        return f"{len(self.__blocks)} mast warship"

    def was_hit(self, coordinates) -> bool:
        """
        Checks if hitting at the passed coordinates would be successful
        """
        if coordinates in self.__blocks:
            self.__hits += 1
            return True
        return False

    def was_sunk(self) -> bool:
        """
        Checks if a warship has been sunk
        """
        return self.__hits == self.__size
