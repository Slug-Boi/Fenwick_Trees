import time
import MatrixSummer as MatrixSum
import MatrixGenerator as mg
import numpy as np
from bit_ds import NdBIT as NDBit
from random import randint
import argparse
import json

twoDTests = 10

matrix_size = 2000

output = {}

test_num = 0



def current_milli_time():
    return round(time.time() * 1000)

def generateData(random_range: tuple[int], max_dimension_size: int, min_dimension_size: int):
    data = []
    for _ in range(2):
        data.append(mg.create_random_ndmatrix((randint(min_dimension_size,max_dimension_size), randint(min_dimension_size,max_dimension_size)), random_range))

    # Add more edge cases
    return data


def randomData(dim: tuple[int], num_test: int, random_range: tuple[int], verbose: bool, json_output: bool):
    lin_times = np.zeros(num_test)
    tree_times = np.zeros(num_test)


    if json_output:
        full_test = {
            "dimension": dim,
            "num_tests": num_test,
            "random_range": random_range,
            "tests": {}
        }

    
    for test in range(num_test):
        testMatrix = np.array(mg.create_random_ndmatrix(dim, random_range), dtype=int)
        fenwick = NDBit(testMatrix, len(dim))
        
        queryPosition = [randint(1, dimension - 1) for dimension in dim]
        
        linearStart = current_milli_time()
        correct = MatrixSum.linear_matrix_sum(testMatrix, [0 for _ in range(len(dim))], queryPosition)
        linearEnd = current_milli_time()
        lin_times[test] = linearEnd - linearStart
        
        fenwickStart = current_milli_time()
        treeResult = fenwick.sum(queryPosition)
        fenwickEnd = current_milli_time()
        tree_times[test] = fenwickEnd - fenwickStart
        
        assert correct == treeResult, f"Assertion failed: correct={correct}, treeResult={treeResult}"
        
        if verbose > 1:
            print(f"[test {test}] Querying to point: {queryPosition}")
            print(f"[test {test}] Linear: time={lin_times[test]}, result={correct}")
            print(f"[test {test}] FenwickTree: time={tree_times[test]}, result={treeResult}")
            print()

        # save individual test results
        if json_output:
            full_test["tests"][test] = {
                "query_position": queryPosition,
                "linear_time": lin_times[test],
                "linear_result": int(correct),
                "fenwick_time": tree_times[test],
                "fenwick_result": treeResult
            }
    
    if verbose > 0:
        print(f"Linear avg: {np.average(lin_times)}")
        print(f"FenwickTree avg: {np.average(tree_times)}")
        print(f"Linear total time: {lin_times.sum()}")
        print(f"Fenwick total time: {tree_times.sum()}")
        print()

    # save run values
    if json_output: 
        full_test["linear_avg"] = np.average(lin_times)
        full_test["fenwick_avg"] = np.average(tree_times)
        full_test["linear_total_time"] = lin_times.sum()
        full_test["fenwick_total_time"] = tree_times.sum()
        global test_num
        output[f"rand {test_num}"] = full_test
        test_num += 1

def oneDFenwickSums():    
    pass

def twoDFenwickSums(testMatrix, queryAmount, MatrixDimensions: tuple[int], verbose: int, json_output: bool):
    testMatrix = np.array(mg.create_random_ndmatrix(MatrixDimensions, random_range),dtype=int)

    buildTimeStart = current_milli_time()
    fenwick = NDBit(testMatrix, 2)
    buildTimeEnd = current_milli_time()

    lin_times = np.zeros(queryAmount)

    tree_times = np.zeros(queryAmount)

    queryPositions = [[randint(1, MatrixDimensions[0]-1), randint(1,MatrixDimensions[1]-1)] for _ in range(queryAmount)]
    
    for i, queryPosition in enumerate(queryPositions):
        linearStart = current_milli_time()
        correct = MatrixSum.linear_matrix_sum(testMatrix, [0,0], queryPosition)
        linearEnd = current_milli_time()
        lin_times[i] = linearEnd - linearStart
        treeStart = current_milli_time()
        treeResult = fenwick.sum(queryPosition)
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

    parser.add_argument(
        '-j',
        '--json',
        action='store_true',
        help="defines if the output should be saved in json format",
        default=False
    )

    args = parser.parse_args()

    #TODO: add fine grain verbose print to only print some tests
    random_range = (-10, 10)
    max_dimension_size = 5000
    min_dimension_size = 500
    
    matrices = generateData(random_range, max_dimension_size, min_dimension_size)
    for testMatrix in matrices:
        matrix_dimension = (randint(min_dimension_size,max_dimension_size), randint(min_dimension_size,max_dimension_size))
        if args.verbose:
            print("Testing 2D Fenwick Tree")
            print("Matrix dimensions:", matrix_dimension)
        twoDFenwickSums(testMatrix,3 ,matrix_dimension, args.verbose, args.json)

        nd_dim = [randint(1,200), randint(1,200),randint(1,200)]

        if args.verbose:
            print("Testing N-D Fenwick Tree")
            print("Matrix dimensions:", nd_dim)

        randomData(nd_dim, 3, random_range, args.verbose, args.json)

    if args.json:
        with open("output.json", "w") as f:
            json.dump(output, f, indent=4)