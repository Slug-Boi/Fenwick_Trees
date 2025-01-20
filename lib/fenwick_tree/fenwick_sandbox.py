import fenwick_tree
# This file is used as a playground file to test the FenwickTree class it does not test the library 

fenwick_tree = fenwick_tree.FenwickTree(5)

print(fenwick_tree.sum(4))

fenwick_tree.update(2, 10)

print(fenwick_tree.sum(4))

fenwick_tree.override_update(2, 10)
print(fenwick_tree.sum(3))