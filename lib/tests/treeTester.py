import time
import MatrixSum
import MatrixGenerator as mg
import numpy as np
from fenwick_tree import NdFenwick as NDBit
from random import randint
import argparse

twoDTests = 10

matrix_size = 2000

def current_milli_time():
    return round(time.time() * 1000)

def generateData(random_range: tuple[int], max_dimension_size: int, min_dimension_size: int):
    data = []
    for _ in range(2):
        data.append(mg.create_random_ndmatrix((randint(min_dimension_size,max_dimension_size), randint(min_dimension_size,max_dimension_size)), random_range))

    # Add more edge cases
    return data


def randomData(dim: tuple[int], num_test: int, random_range: tuple[int], verbose: bool):
    lin_times = np.zeros(num_test)
    tree_times = np.zeros(num_test)
    
    for test in range(num_test):
        testMatrix = np.array(mg.create_random_ndmatrix(dim, random_range), dtype=int)
        fenwick = NDBit(testMatrix, len(dim))
        
        queryPosition = [randint(1, dimension - 1) for dimension in dim]
        
        linearStart = current_milli_time()
        correct = MatrixSum.NDSumArray(testMatrix, len(dim), [0 for _ in range(len(dim))], queryPosition)
        linearEnd = current_milli_time()
        lin_times[test] = linearEnd - linearStart
        
        fenwickStart = current_milli_time()
        treeResult = fenwick.sum_query(queryPosition)
        fenwickEnd = current_milli_time()
        tree_times[test] = fenwickEnd - fenwickStart
        
        assert correct == treeResult, f"Assertion failed: correct={correct}, treeResult={treeResult}"
        
        if verbose > 1:
            print(f"[test {test}] Querying to point: {queryPosition}")
            print(f"[test {test}] Linear: time={lin_times[test]}, result={correct}")
            print(f"[test {test}] FenwickTree: time={tree_times[test]}, result={treeResult}")
            print()
    
    if verbose > 0:
        print(f"Linear avg: {np.average(lin_times)}")
        print(f"FenwickTree avg: {np.average(tree_times)}")
        print(f"Linear total time: {lin_times.sum()}")
        print(f"Fenwick total time: {tree_times.sum()}")
        print()

def oneDFenwickSums():    
    pass

def twoDFenwickSums(testMatrix, queryAmount, MatrixDimensions: tuple[int], verbose: int):
    testMatrix = np.array(mg.create_random_ndmatrix(MatrixDimensions, random_range),dtype=int)

    buildTimeStart = current_milli_time()
    fenwick = NDBit(testMatrix, 2)
    buildTimeEnd = current_milli_time()

    lin_times = np.zeros(queryAmount)

    tree_times = np.zeros(queryAmount)

    queryPositions = [[randint(1, MatrixDimensions[0]-1), randint(1,MatrixDimensions[1]-1)] for _ in range(queryAmount)]
    
    for i, queryPosition in enumerate(queryPositions):
        linearStart = current_milli_time()
        correct = MatrixSum.NDSumArray(testMatrix, 2, [0,0], queryPosition)
        linearEnd = current_milli_time()
        lin_times[i] = linearEnd - linearStart
        treeStart = current_milli_time()
        treeResult = fenwick.sum_query(queryPosition)
        treeEnd = current_milli_time()
        tree_times[i] = treeEnd - treeStart

        if verbose > 1:
            print(f"[test {i}] Querying to point: {queryPosition}")
            print(f"[test {i}] Linear: time={lin_times[i]}, result={correct}")
            print(f"[test {i}] FenwickTree: time={tree_times[i]}, result={treeResult}")


        assert correct == treeResult, f"Assertion failed: correct={correct}, treeResult={treeResult}"

    if verbose > 0:
        print(f"Fenwick Tree build time: {buildTimeEnd - buildTimeStart}")
        print(f"Quering to points: {queryPositions}")
        print(f"Linear avg: {np.average(lin_times)}")
        print(f"FenwickTree avg: {np.average(tree_times)}")
        print(f"Linear total time: {lin_times.sum()}")
        print(f"Fenwick total time: {tree_times.sum()}")
        print()


def nDFenwickSums():
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-v',
        '--verbose',
        nargs='?',
        const=1,
        type=int,
        help="defines the level of verbosity of the output",
        default=0
    )

    args = parser.parse_args()

    #TODO: add fine grain verbose print to only print some tests
    random_range = (-10, 10)
    max_dimension_size = 2000
    min_dimension_size = 500
    
    matrices = generateData(random_range, max_dimension_size, min_dimension_size)
    for testMatrix in matrices:
        matrix_dimension = (randint(min_dimension_size,max_dimension_size), randint(min_dimension_size,max_dimension_size))
        if args.verbose:
            print("Testing 2D Fenwick Tree")
            print("Matrix dimensions:", matrix_dimension)
        twoDFenwickSums(testMatrix,3 ,matrix_dimension, args.verbose)

        nd_dim = [randint(1,200), randint(1,200),randint(1,200)]

        if args.verbose:
            print("Testing N-D Fenwick Tree")
            print("Matrix dimensions:", nd_dim)

        randomData(nd_dim, 3, random_range, args.verbose)