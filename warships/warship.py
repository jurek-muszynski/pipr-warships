class Warship():
    """
    Warship class. Represents a single warship on the board,
    consisting of [1-5] blocks

    :param blocks: Represents the lists of blocks
    :type blocks: list[tuple[int, int]]

    :param size: Represents warship's size.
    :type size: int

    :param hits: Represents warship's hit count
    :type hits: int

    :param hit_blocks: Represents warships blocks that were hit
    :type hit_blocks: list[tuple[int, int]]
    """

    def __init__(self, blocks: list[tuple[int, int]]) -> None:
        """
        Creates an instance of the warship class.\n
        Raises ValueError if passed blocks are invalid.\n

        :param blocks: blocks of coordinates, that a warships is made of
        :type blocks: list[tuple[int, int]]
        """
        if not blocks:
            raise ValueError("Warship cannot be empty")
        elif not self.evaluate_blocks(blocks):
            raise ValueError("Invalid blocks")
        else:
            self.__blocks = blocks
        self.__size = len(blocks)
        self.__hits = 0
        self.__hit_blocks = []

    @property
    def blocks(self):
        return self.__blocks

    @property
    def size(self) -> int:
        return self.__size

    @property
    def hits(self) -> int:
        return self.__hits

    def evaluate_blocks(self, blocks: list[tuple[int, int]]) -> bool:
        """
        Checks if passed blocks are correctly alligned
        (distance between two consecutive blocks is 1)

        :param blocks: blocks of coordinates
        :type blocks: list[tuple[int, int]]
        """
        for x, y in blocks:
            if (x < 0 or y < 0):
                return False
        for i in range(len(blocks)-1):
            x_i, y_i = blocks[i]
            x_ii, y_ii = blocks[i+1]
            if abs(x_i - x_ii) + abs(y_i - y_ii) != 1:
                return False
        return True

    def __str__(self) -> str:
        """
        Returns a simple description of a warship:
        {1-5} mast warship
        """
        return f"{len(self.__blocks)} mast warship"

    def was_hit(self, location: tuple[int, int]) -> bool:
        """
        Hits the warship at the following coordinates\n
        Returns True if the hit was successful\n
        Returns False if the hit was a miss

        :param location: coordinates e.g. (1,1)
        :type location: tuple[int]
        """
        if location in self.__blocks and location not in self.__hit_blocks:
            self.__hits += 1
            self.__hit_blocks.append(location)
            return True
        return False

    def was_sunk(self) -> bool:
        """
        Checks if a warship has been sunk
        """
        return self.__hits == self.__size
