class BIT:
    """
    A class representing a Binary Indexed Tree (Fenwick Tree).
    The tree is 1 indexed and the input array is 0 indexed.

    :param input: input array to build the tree
    """ 
    def __init__(self, input: list) -> BIT: ...

    @classmethod
    def update(self, position: int, val: int) -> None:
        """
        Updates the Fenwick Tree with a given value at a specified position.
        position is 0 indexed.

        :param position: index of the element to be updated
        :param val: value to be added to the specified position
        """


class NdBIT:
    """
    A class representing a N-Dimensional BIT (Fenwick Tree).
    The tree is 1 indexed and the input array is 0 indexed.

    :param input: input array to build the tree
    :param dim: number of dimensions of the input array
    """
    def __init__(self, input: list, dim: int) -> NdBIT: ...

    @classmethod
    def update(self, position: list[int], val: int) -> None:
        """
        Updates the Fenwick Tree with a given value at a specified position.
        position is 0 indexed.

        :param position: list of indices representing the position in the N-dimensional array
        :param val: value to be added to the specified position
        """
    @classmethod
    def tree(self) -> list:
        """
        Returns the BIT tree.
        """

    @classmethod
    def get_size(self) -> int:
        """
        Returns the size of the BIT
        """

    @classmethod
    def get_dim(self) -> int:
        """
        Returns the number of dimensions of the Fenwick Tree
        """

    @classmethod
    def sum_query(self, position: list[int]) -> int:
        """
        Returns the sum of the elements from the origin to the specified position.
        position is 0 indexed.

        :param position: list of indices representing the position in the N-dimensional array
        """

    @classmethod
    def range_sum_query(self, start: list[int], end: list[int]) -> int:
        """
        Returns the sum of the elements in the specified range.
        start and end are 0 indexed.

        :param start: list of indices representing the start position in the N-dimensional array
        :param end: list of indices representing the end position in the N-dimensional array
        """