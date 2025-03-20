import MatrixGenerator
import time
import numpy as np

def print2DMatrix(matrix):
    for row in matrix:
        print(row)

#print2DMatrix(MatrixGenerator.create_random_ndmatrix((4,5,3), (0, 10)))

# startLin = time.time()
# MatrixGenerator.create_random_ndmatrix((5000,5000), (0, 10))
# endLin = time.time()

# startAsync = time.time()
# MatrixGenerator.create_random_ndmatrix_async((5000,5000), (0, 10))
# endAsync = time.time()

start_numpy = time.time()
mat = MatrixGenerator.create_random_ndmatrix_better((5000,5000), (0, 10))
end_numpy = time.time()

#print2DMatrix(mat)

print("Numpy: ", end_numpy - start_numpy)
# print("Linear: ", endLin - startLin)
# print("Async: ", endAsync - startAsync)
