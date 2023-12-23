class Warship():
    """
    Warship class. Represents a single warship on the board,
    consisting of [1-5] blocks

    :param blocks: Represents the lists of blocks
    :type blocks: list[int]

    :param size: Represents warship's size.
    :type size: int

    :param hits: Represents warship's hit count
    :type hits: int
    """

    def __init__(self, blocks: list[int]) -> None:
        """
        Creates an instance of a warship.
        Raises ValueError if passed blocks are invalid.
        """
        if not blocks:
            raise ValueError("Warship cannot be empty")
        else:
            self.__blocks = blocks
        self.__size = len(blocks)
        self.__hits = 0

    @property
    def blocks(self):
        return self.__blocks

    @property
    def size(self) -> int:
        return self.__size

    @property
    def hits(self) -> int:
        return self.__hits

    def __str__(self) -> str:
        """
        Returns a sample description of a warship:
        {1-5} mast warship
        """
        return f"{len(self.__blocks)} mast warship"

    def was_hit(self, coordinates) -> bool:
        """
        Checks if hitting the following coordinates was successful
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