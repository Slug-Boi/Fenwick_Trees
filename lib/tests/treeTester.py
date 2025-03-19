import time
import MatrixSum
import testDataGenerator
from ndFenwick.ndfenwick import NDBit
from random import randint
import argparse

twoDTests = 10

matrix_size = 2000

def current_milli_time():
    return round(time.time() * 1000)

def randomData(dim: tuple[int], num_test: int, random_range: tuple[int], debug_print: bool):
    for test in range(num_test):
        testMatrix = testDataGenerator.CreateRandomNDMatrix(dim, random_range)
        fenwick = NDBit(testMatrix, len(dim))
        
        queryPosition = [randint(1, dimension-1) for dimension in dim]
        
        linearStart = current_milli_time()
        correct = MatrixSum.NDSumArray(testMatrix, len(dim), [0 for _ in range(len(dim))], queryPosition)
        linearEnd = current_milli_time()
        linearTime = linearEnd - linearStart
        fenwickStart = current_milli_time()
        treeResult = fenwick.getSum(queryPosition)
        fenwickEnd = current_milli_time()
        fenwickTime = fenwickEnd - fenwickStart
        if debug_print:
            print(f"[test {test}] Querying to point: {queryPosition}")
            print(f"[test {test}] Linear: time={linearTime}, result={correct}")
            print(f"[test {test}] FenwickTree: time={fenwickTime}, result={treeResult}")
            print()
        assert correct == treeResult

def oneDFenwickSums():    
    pass

def twoDFenwickSums(MatrixDimensions: tuple[int], random_range: tuple[int, int], debug_print: bool):
    testMatrix = testDataGenerator.CreateRandomNDMatrix(MatrixDimensions, random_range)
    fenwick = NDBit(testMatrix, 2)
    
    queryPosition = [randint(1, MatrixDimensions[0]-1), randint(1,MatrixDimensions[1]-1)]
    
    linearStart = current_milli_time()
    correct = MatrixSum.NDSumArray(testMatrix, 2, [0,0], queryPosition)
    linearEnd = current_milli_time()
    linearTime = linearEnd - linearStart
    treeStart = current_milli_time()
    treeResult = fenwick.getSum(queryPosition)
    treeEnd = current_milli_time()
    treeTime = treeEnd - treeStart
    if debug_print:
        print(f"Quering to point: {queryPosition}")
        print(f"Linear: time={linearTime}, result={correct}")
        print(f"FenwickTree: time={treeTime}, result={treeResult}")
        print()
    assert correct == treeResult

def nDFenwickSums():
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-dp',
        '--debug_print',
        action=argparse.BooleanOptionalAction,
        help="toggles to debug output print of the tests",
        default=False
    )

    args = parser.parse_args()

    #TODO: add fine grain debug print to only print some tests
    random_range = (-10, 10)
    max_dimension_size = 2000
    min_dimension_size = 500
    for _ in range(10):
        matrix_dimension = (randint(min_dimension_size,max_dimension_size), randint(min_dimension_size,max_dimension_size))
        if args.debug_print:
            print("Matrix dimensions:", matrix_dimension)
        twoDFenwickSums(matrix_dimension, random_range, args.debug_print)

    randomData((randint(1,200), randint(1,200), randint(1,200)), 10, (-10, 10), args.debug_print)