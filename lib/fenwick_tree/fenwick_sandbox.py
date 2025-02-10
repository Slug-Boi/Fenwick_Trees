import fenwick_tree
# This file is used as a playground file to test the FenwickTree class it does not test the library 

fenwick_tree = fenwick_tree.FenwickTree([4,8,5,2,6,1,0,8])

print(fenwick_tree.get_tree())

print(fenwick_tree.sum(2))

fenwick_tree.update(2, 10)

print(fenwick_tree.sum(2))

fenwick_tree.override_update(2, 10)

print(fenwick_tree.sum(2))

#print(fenwick_tree.get_tree())

newtree = fenwick_tree.new_file("test.txt")

print(newtree.get_tree())

print(newtree.get_sum_indices(3))