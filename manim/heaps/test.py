from heapq import *


arr = [3, 2, -3, 6, 5, 4, -2, 7]

edges = []

for i in range(len(arr)):
    if i == 0:
        continue
    parent = (i - 1) // 2
    edges.append((parent, i))
    child1 = 2 * i + 1
    child2 = 2 * i + 2
    if child1 < len(arr):
        edges.append((i, child1))
    if child2 < len(arr):
        edges.append((i, child2))

print("Edges:", edges)