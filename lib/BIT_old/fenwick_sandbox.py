import time
import MatrixGenerator as mg
import bit_ds as fenwick_tree
import numpy as np
# This file is used as a playground file to test the FenwickTree class it does not test the library 

# fenwick_tree = fenwick_tree.FenwickTree([4,8,5,2,6,1,0,8])

# print(fenwick_tree.get_tree())

# print(fenwick_tree.sum(2))

# fenwick_tree.update(2, 10)

# print(fenwick_tree.sum(2))

# fenwick_tree.override_update(2, 10)

# print(fenwick_tree.sum(2))

# #print(fenwick_tree.get_tree())

# newtree = fenwick_tree.new_file("test.txt")

# print(newtree.get_tree())

# print(newtree.get_sum_indices(3))

tree = fenwick_tree.BIT([4,8,5,2,6,1,0,8])
print(tree.size)




data = mg.create_random_ndmatrix((500,500), (0, 10))

starttime = time.time()
fenwick_tree = fenwick_tree.NdBIT(np.array(data,dtype=int), 2)
stoptime = time.time()


# print(stoptime - starttime)
#print(fenwick_tree.get_tree())
#print(fenwick_tree.sum_query([1,0]))

# print(fenwick_tree.range_sum_query([0,0],[1,1]))
# fenwick_tree.range_sum_query