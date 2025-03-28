@staticmethod
def linear_matrix_sum(array: list, position1: list[int], position2: list[int]) -> int:
    """
    Linearly sum the values of a submatrix defined by two points.
    The points are defined as n-dimensional coordinates. E.g. for a 3D matrix [x,y,z]

    :param array: N-dimensional array to sum
    :param start: starting position of the submatrix
    :param end: ending position of the submatrix
    :return: sum of the submatrix
    """