use pyo3::{prelude::*, types::PyString};
use std::fs;
use std::io::prelude::*;
use rayon::{option, prelude::*, string};

/// A Python module implemented in Rust.
#[pymodule]
fn fenwick_tree(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<FenwickTree>()?;
    Ok(())
}


// Current code is heavily based on the implementation of Fenwick Tree in GeeksforGeeks
// https://www.geeksforgeeks.org/binary-indexed-tree-or-fenwick-tree-2/
// https://www.geeksforgeeks.org/fenwick-tree-for-competitive-programming/?ref=ml_lbp


// Important note here is that the tree is 1 indexed, so the first element is at index 1
// BUT when making range or sum calls the input index is 0 indexed so a tree of size 5 will have valid indices 0, 1, 2, 3, 4
fn index_check(index: i32, size: usize) {
    if index >= 0 || index < size as i32 {
        return
    }
    panic!("Index out of bounds {}, size {}", index, size);
}

// Fenwick tree is represented using a Vector
#[pyclass]
struct FenwickTree {
    tree: Vec<i32>,
    size: i32
}

#[pymethods]
impl FenwickTree {
    // Adds value to the current value at index (this is the update outlined by the geeksforgeeks article)
    fn update(&mut self, mut index: i32, value: i32) {
        // 1 indexed cause that just how it be
        index = index + 1;
        index_check(index, self.tree.len());

        while index <= (self.tree.len()-1) as i32 {
            self.tree[index as usize] += value;
            index += index & (-index);
        }
    }

    fn get_size(&self) -> i32 {
        self.size
    }

    fn get_tree(&self) -> Vec<i32> {
        self.tree.clone()
    }

    // This function behaves more like what you would expect from an update function where it overides the value at index
    // And then propagates the change up the tree. NOTE: Be careful as this may result in negative values in the tree
    // so please exercise caution when using this
    fn override_update(&mut self, mut index: i32, value: i32) {
        
        // 1 indexed cause that just how it be
        index = index + 1;
        index_check(index, self.tree.len());

        let diff = value - self.tree[index as usize];

        while index <= (self.tree.len()-1) as i32 {
            self.tree[index as usize] += diff;
            index += index & (-index);
        }
    }

    // Base constructor for the fenwick tree. Takes a vector of i32s and constructs the tree
    #[new]
    fn new(input: Vec<i32>) -> Self {
        let size = input.len() as i32;
        let mut tree = vec![0; size as usize];
        tree.insert(0, -9999); // Placeholder value to make the tree 1 indexed
        let mut fenwick_tree = FenwickTree { tree, size };
        for x in 0..size {
            fenwick_tree.update(x, input[x as usize]);
        }           

        return fenwick_tree;
    }
    
    // Constructor for the fenwick tree that takes a file path and constructs the tree
    #[staticmethod]
    fn new_file(path: String) -> Self {
        let input: Vec<i32> = fs::read_to_string(path)
            .expect("Something went wrong reading the file")
            .split_whitespace()
            .map(|x| x.parse::<i32>().unwrap())
            .collect();

    let size = input.len() as i32;
    let mut tree = vec![0; size as usize];
    tree.insert(0, -9999); // Placeholder value to make the tree 1 indexed
    let mut fenwick_tree = FenwickTree { tree, size };
    for x in 0..size {
        fenwick_tree.update(x, input[x as usize]);
    }
    fenwick_tree
    }

    fn sum(&self, mut index: i32) -> i32 {
        // 1 indexed cause that just how it be
        index = index + 1;
        let mut sum = 0;

        while index > 0 {
            sum += self.tree[index as usize];
            index -= index & -index;
        }

        // sum = self.tree
        //     .par_iter().step_by((index & -index) as usize)
        //     .filter_map(|&i| if i > 0 {Some(self.tree[i as usize])} else {None})
        //     .sum();

        //Parallelize the sum calculation using Rayon
        // sum = (1..=index).collect::<Vec<_>>()
        //     .into_par_iter().step_by((index & -index) as usize)
        //     .filter_map(|i| if i > 0 {Some(self.tree[(i) as usize])} else {None})
        //     .sum();

        sum
    }

    // Returns a vector of indices that are used to calculate the sum of the elements in the range [0, index]
    fn get_sum_indices(&self, mut index: i32) -> Vec<i32> {
        // 1 indexed cause that just how it be
        index = index + 1;
        let mut indices = Vec::new();

        while index > 0 {
            indices.push(index);
            index -= index & -index;
        }

        indices
    }

    // Returns a vector of indices that are used to calculate the sum of the elements in the range [left, right]
    fn get_range_sum_indices(&self, left: i32, right: i32) -> Vec<i32> {
        let mut left_indices = self.get_sum_indices(left - 1);
        let mut right_indices = self.get_sum_indices(right);

        left_indices.append(&mut right_indices);
        left_indices
    }

    // Returns the sum of the elements in the range [left, right]
    fn range_sum(&self, left: i32, right: i32) -> i32 {
        self.sum(right) - self.sum(left - 1)
    }
}