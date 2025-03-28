@staticmethod
def create_random_ndmatrix(dim: list[int], random_range: tuple[int, int]) -> list:
    """
    Create a N-Dimensional matrix with random values.

    :param dim: list of dimensions of the matrix e.g. for a matrix of size 3x4x5, dim = [3,4,5]
    :param random_range: tuple of range of random value bounds (min, max)
    """

@staticmethod
def create_random_ndmatrix_async(dim: list[int], random_range: tuple[int, int]) -> list:
    """
    Asynchronously create a N-Dimensional matrix with random values.
    WARNING: This function is currently much slower than the synchronous version.
    if you decide to use it make sure input is large enough to justify the overhead.

    :param dim: list of dimensions of the matrix e.g. for a matrix of size 3x4x5, dim = [3,4,5]
    :param random_range: tuple of range of random value bounds (min, max)
    """
