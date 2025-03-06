from copy import copy
 
class NDBit:
    """
    input: n-dimensional array  
    dimensions: The number of dimensions in the input array
    """
    def __init__(self, input, dimensions):
        self.startInput = input
        self.dimensions = dimensions
        self.BIT = self.CreateEmptyBIT(dimensions, input)
        self.FillTree(dimensions, input, [])
    
    def CreateEmptyBIT(self, dimension, array):
        if dimension == 1:
            return [0 for _ in range(len(array)+1)]
        bit = []
        for i in range(len(array)+1):
            bit.append(self.CreateEmptyBIT(dimension-1, array[0]))
        return bit
    
    def FillTree(self, dimension, array, position: list):
        if dimension == 1:
            for i in range(len(array)):
                tempPos = copy(position)
                tempPos.append(i)
                self.Update(tempPos, array[i])
            return
        
        for i in range(len(array)):
            tempPos = copy(position)
            tempPos.append(i)
            self.FillTree(dimension-1, array[i], tempPos)
        
    def Update(self, position: list, val: int):
        def UpdateHelper(position, val, array):
            dimension = position[0]
            while dimension < len(array):
                if len(position) != 1:
                    UpdateHelper(position[1:], val, array[dimension])
                else:
                    array[dimension] += val
                dimension += (dimension & -dimension)
        
        position = list(map(lambda x: x+1, position))
        UpdateHelper(position, val, self.BIT)
 
    def getSum(self, position: list):
        def SumHelper(position, array):
            sum = 0
            dimension = position[0]
            while dimension > 0:
                if len(position) != 1:
                    sum += SumHelper(position[1:], array[dimension])
                else:
                    sum += array[dimension]
                dimension -= (dimension & -dimension)
            return sum
 
        position = list(map(lambda x: x+1, position))
        return SumHelper(position, self.BIT)