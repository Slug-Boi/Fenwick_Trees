from random import randint

def CreateRandom2DMatrix(size: int, random_range: tuple[int, int]) -> list[list[int]]:
    return [[randint(random_range[0], random_range[1]) for _ in range(size)] for _ in range(size)] 

def CreateRandomNDMatrix(dimensions: tuple[int], random_range: tuple[int, int]) -> list:
    def recursionHelper(dimensions: tuple[int]) -> list:
        dimension = dimensions[0]
        if len(dimensions) == 1:
            return [randint(random_range[0], random_range[1]) for _ in range(dimension)]
        array = []
        for _ in range(dimension):
            array.append(recursionHelper(dimensions[1:]))
        
        return array
    return recursionHelper(dimensions)

def print2DMatrix(matrix):
    for row in matrix:
        print(row)

if __name__ == "__main__":
    random_range = [0, 10]       

    print2DMatrix(CreateRandomNDMatrix((4,5,3,2), random_range))
    