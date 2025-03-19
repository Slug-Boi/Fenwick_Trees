import MatrixGenerator
import time

def print2DMatrix(matrix):
    for row in matrix:
        print(row)

#print2DMatrix(MatrixGenerator.create_random_ndmatrix((4,5,3), (0, 10)))

startLin = time.time()
MatrixGenerator.create_random_ndmatrix((5000,5000), (0, 10))
endLin = time.time()

startAsync = time.time()
MatrixGenerator.create_random_ndmatrix_async((5000,5000), (0, 10))
endAsync = time.time()

print("Linear: ", endLin - startLin)
print("Async: ", endAsync - startAsync)
