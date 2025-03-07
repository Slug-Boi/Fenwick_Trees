from random import randint

class TwoDBIT:
    def __init__(self, matrix: list[list[int]], matrix_size: int) -> None:
        self.startMatrix = matrix
        self.matrix_size = matrix_size
        self.BIT = [[0 for j in range(matrix_size+1)] for i in range(matrix_size+1)]
    
    # Not actually needed. But it's here now :)
    @staticmethod 
    def transpose(matrix: list[list[int]]) -> list[list[int]]:
        aux = [[0 for _ in range(len(matrix))] for _ in range(len(matrix[0]))]
        for j in range(len(matrix)):
            for i in range(len(matrix[0])):
                aux[i][j] = matrix[(len(matrix)-1) - j][i]
        return aux
    
    def Create(self):
        aux = self.startMatrix
        for row in range(self.matrix_size):
            for col in range(self.matrix_size):
                self.Update(row, col, aux[row][col])

    def CreatePositions(self) -> list:
        operations = []
        for row in range(self.matrix_size):
            for col in range(self.matrix_size):
                operations.append(((row, col), self.UpdatePositions(row, col, self.startMatrix[row][col])))
        return operations

    def Update(self, x: int, y: int, val: int) -> None:
        x += 1
        y += 1
        while x <= self.matrix_size:
            loop_y = y # Reset loop_y on every new x value
            while loop_y <= self.matrix_size:
                self.BIT[x][loop_y] += val
                loop_y += (loop_y & -loop_y) # Add lsb to loop_y
            x += (x & -x) # Add lsb to x
    
    def UpdatePositions(self, x: int, y: int, val: int) -> list:
        x += 1
        y += 1
        updateIndeces = []
        while x <= self.matrix_size:
            loop_y = y # Reset loop_y on every new x value
            while loop_y <= self.matrix_size:
                self.BIT[x][loop_y] += val
                updateIndeces.append((x, loop_y))
                loop_y += (loop_y & -loop_y) # Add lsb to loop_y
            x += (x & -x) # Add lsb to x
        return updateIndeces

    def getSum(self, x: int, y: int) -> int:
        x += 1
        y += 1
        sum = 0
        while x > 0:
            loop_y = y
            while loop_y > 0:
                sum += self.BIT[x][loop_y]
                loop_y -= (loop_y & -loop_y) # Add lsb to loop_y
            x -= (x & -x) # Add lsb to x
        return sum

    def getSumPositions(self, x: int, y: int) -> tuple[int, list[tuple[int,int]]]:
        x += 1
        y += 1
        sum = 0
        sumIndeces = []
        while x > 0:
            loop_y = y
            while loop_y > 0:
                sum += self.BIT[x][loop_y]
                sumIndeces.append((x, loop_y))
                loop_y -= (loop_y & -loop_y) # Add lsb to loop_y
            x -= (x & -x) # Add lsb to x
        return sum, sumIndeces
    
    def SquareSum(self, point1: tuple[int, int], point2: tuple[int, int]) -> int:
        s1 = self.getSum(point2[0], point2[1]) # Full box
        s2 = self.getSum(point2[0], point1[1]-1) # Left box
        s3 = self.getSum(point1[0]-1, point2[1]) # Top box
        s4 = self.getSum(point1[0]-1, point1[1]-1) # Overlap box
        
        result = s1 - s2 - s3 + s4
        return result
    

    """
    return: result, Full box, Left box, Top, Overlap box
    """
    def SquareSumPositions(self, point1: tuple[int, int], point2: tuple[int, int]):
        s1 = self.getSum(point2[0], point2[1]) # Full box
        s2 = self.getSum(point2[0], point1[1]-1) # Left box
        s3 = self.getSum(point1[0]-1, point2[1]) # Top box
        s4 = self.getSum(point1[0]-1, point1[1]-1) # Overlap box
        
        result = s1 - s2 - s3 + s4
        return result, (point2[0], point2[1]), (point2[0], point1[1]-1), (point1[0]-1, point2[1]), (point1[0]-1, point1[1]-1)

    def PrintBit(self):
        for row in self.BIT:
            print(row)
    
    def getBIT(self):
        return self.BIT


def CreateRandomMatrix(size: int, random_range: tuple[int, int]) -> list[list[int]]:
    return [[randint(random_range[0], random_range[1]) for _ in range(size)] for _ in range(size)]    

def PrintMatrix(matrix):
    for row in matrix:
        print(row)

if __name__ == "__main__":
    M2 = [
        [3,  4,  0],
        [8,  11, 10],
        [9,  7,  5],
    ]
    M_size = 6
    M = CreateRandomMatrix(M_size, (0, 20))
    PrintMatrix(M)
    bit = TwoDBIT(M2, 3)
    # bit.PrintBitMap()
    # bit.PrintBit()
    print("\n"*2)
    bit.Create()
    bit.PrintBit()
    # print("\n"*2)
    # print("Query: sum(0, 0) =", bit.getSum(0, 0))
    # print("Query: sum(1, 1) =", bit.getSum(1, 1))
    # print("Query: sum(0, 2) =", bit.getSum(0, 2))
    # print("Query: sum(2, 0) =", bit.getSum(2, 0))
    # print("Query: sum((1,1), (2,2)) =", bit.SquareSum((1,1), (2,2)))
    # print("Query: sum((1,1), (4,3)) =", bit.SquareSum((1,1), (4,3)))