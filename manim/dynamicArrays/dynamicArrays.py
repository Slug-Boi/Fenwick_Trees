import sys
from ndfenwick import *
from fenwick_tree import *

# Rotating arrays in python

# Split the array in smaller arrays that are N long
def split(arr, n) -> list:
    result = []
    for i in range(0, len(arr), n):
        result.append(arr[i:i+n])
    return result

arr = [1,2,3,4,5,6,7]
fenwick = NdFenwick(arr, 1)

arr = split(arr, 4)

matrix = [[1,2,3], [4,5,6], [7,8,9]]


print(fenwick.get_tree())


#print(arr)
