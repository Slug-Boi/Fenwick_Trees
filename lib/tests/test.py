import MatrixGenerator
import MatrixSummer as ms
import time
import numpy as np
from fenwick_tree import NdFenwick as NDBit
import MatrixSum as old_ms
import fenwick_tree

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

# start_numpy = time.time()
# mat = MatrixGenerator.create_random_ndmatrix_better((5000,5000), (0, 10))
# end_numpy = time.time()

#print2DMatrix(mat)

#print("Numpy: ", end_numpy - start_numpy)
# print("Linear: ", endLin - startLin)
# print("Async: ", endAsync - startAsync)

data = MatrixGenerator.create_random_ndmatrix((2000,2000), (0, 10))

data = np.array(data, dtype=int)

fenwick = NDBit(data, 2)

fenwick_time = time.time()
fen_result = fenwick.sum_query((1999, 1999))
fenwick_time_end = time.time()

print("Fenwick: ", fenwick_time_end - fenwick_time)
print("result", fen_result)

linear_time = time.time()
sm = ms.linear_matrix_sum(data, (0,0), (1999,1999))
linear_time_end = time.time()

print("Linear: ", linear_time_end - linear_time)
print("result", sm)

old_time = time.time()
old_result = old_ms.NDSumArray(data, 2, [0,0], [1999,1999])
old_time_end = time.time()

print("Old: ", old_time_end - old_time)
print("result", old_result)

# startLin = time.time()
# output_mat = MatrixGenerator.create_random_ndmatrix((2000,2000), (0, 10))
# endLin = time.time()

# startPyBuilder = time.time()
# fenwick_slow = NDBit(output_mat, 2)
# endPyBuilder = time.time()

# startRustBuilder = time.time()
# fenwick = fenwick_tree.NdFenwick(np.array(output_mat,dtype=int), 2)
# endRustBuilder = time.time()

# print("Linear Data Generation: ", endLin - startLin)
# print("PyBuilder: ", endPyBuilder - startPyBuilder)
# print("RustBuilder: ", endRustBuilder - startRustBuilder)
