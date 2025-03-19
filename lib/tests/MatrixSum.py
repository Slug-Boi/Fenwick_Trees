def NDSumArray(array: list, dimensions: int, position1: list[int], position2: list[int]) -> int:
    if len(position1) != dimensions or len(position2) != dimensions:
        raise Exception("Length of positional arguments don't match dimentions of array")
    if len(position1) != len(position2):
        raise Exception("Amount of positional arguments for position1 does not match position2")
    
    def SumHelper(position1, position2, array):
        sum = 0
        for i in range(position1[0], position2[0]+1, 1):
            if len(position1) == 1:
                sum += array[i]
            else:
                sum += SumHelper(position1[1:], position2[1:], array[i])
        return sum
    
    return SumHelper(position1, position2, array)

if __name__ == "__main__":
    M3 = [
        [[2, 4, 2], [19, 2, 1], [0, 12, 2]],
        [[19, 2, 4], [8, 8, 9], [1, 4, 12]],
        [[2, 10, 1], [4, 20, 1],  [10, 3, 1]],
    ]
    M33 = [
        [[1,1,1], [1,1,1], [1,1,1]],
        [[1,1,1], [1,1,1], [1,1,1]],
        [[1,1,1], [1,1,1], [1,1,1]]
    ]
    M2 = [
        [3,  4,  0],
        [8,  11, 10],
        [9,  7,  5],
    ]

    print(NDSumArray(M2, 2, [1,1], [2,2]))