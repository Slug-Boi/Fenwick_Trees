use pyo3::prelude::*;
use std::fs;
use ndarray::{Array, ArrayView, ArrayViewMut, IxDyn};
use numpy::{IntoPyArray, PyArray, PyReadonlyArrayDyn};

/// A Python module implemented in Rust.
#[pymodule]
fn bit_ds(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<BIT>()?;
    m.add_class::<NdBIT>()?;
    Ok(())
}

// Current code is heavily based on the implementation of Fenwick Tree in GeeksforGeeks
// https://www.geeksforgeeks.org/binary-indexed-tree-or-fenwick-tree-2/
// https://www.geeksforgeeks.org/fenwick-tree-for-competitive-programming/?ref=ml_lbp


// Important note here is that the tree is 1 indexed, so the first element is at index 1
// BUT when making range or sum calls the input index is 0 indexed so a tree of size 5 will have valid indices 0, 1, 2, 3, 4
fn index_check(index: i32, size: usize) {
    if index >= 0 && index < size as i32 {
        return;
    }
    panic!("Index out of bounds {}, size {}", index, size);
}

// Fenwick tree is represented using a Vector
#[pyclass]
struct BIT {
    #[pyo3(get)]
    tree: Vec<i32>,
    #[pyo3(get)]
    size: i32
}

#[pymethods]
impl BIT {
    // Adds value to the current value at index (this is the update outlined by the geeksforgeeks article)
    fn update(&mut self, mut index: i32, value: i32) {
        // 1 indexed cause that just how it be
        index = index + 1;
        index_check(index, self.tree.len());

        while index < (self.tree.len()) as i32 {
            self.tree[index as usize] += value;
            index += index & (-index);
        }
    }

    // This function behaves more like what you would expect from an update function where it overides the value at index
    // And then propagates the change up the tree. NOTE: Be careful as this may result in negative values in the tree
    // so please exercise caution when using this
    fn override_update(&mut self, index: i32, value: i32) {
        let diff = value - self.tree[index as usize];
        
        // Update the value at index
        self.update(index, diff);
    }

    // Base constructor for the fenwick tree. Takes a vector of i32s and constructs the tree
    #[new]
    fn new(input: Vec<i32>) -> Self {
        let size = input.len() as i32;
        let mut tree = vec![0; size as usize];
        tree.insert(0, -9999); // Placeholder value to make the tree 1 indexed
        let mut bit = BIT { tree, size };
        for x in 0..size {
            bit.update(x, input[x as usize]);
        }           

        return bit;
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
    let mut bit = BIT { tree, size };
    for x in 0..size {
        bit.update(x, input[x as usize]);
    }
    bit
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
    fn sum_indices(&self, mut index: i32) -> Vec<i32> {
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
    fn range_sum_indices(&self, left: i32, right: i32) -> Vec<i32> {
        let mut left_indices = self.sum_indices(left - 1);
        let mut right_indices = self.sum_indices(right);

        left_indices.append(&mut right_indices);
        left_indices
    }

    // Returns the sum of the elements in the range [left, right]
    fn range_sum(&self, left: i32, right: i32) -> i32 {
        self.sum(right) - self.sum(left - 1)
    }
}

// This is an n-dimensional fenwick tree that is used to store the sum of elements in a n-dimensional array
// The tree is the nested arrays that store the sum of elements
// The tree is 1 indexed in all dimensions
// dimensions is the number of dimensions of the tree
// The size is a vector of the n-th dimension sizes
#[pyclass]
struct NdBIT {
    // Cannot define pyo3 getter due to conversion error need to manually define getter here
    tree: Array<i64, IxDyn>,
    #[pyo3(get)]
    dim: i32,
    #[pyo3(get)]
    size: i32
}

/* 
    NdFenwick Tree generalised functions. We want to use slices and other rust based functions
    to make the code more efficient but pyo3 requires extensions to these base structures
    so instead we define them here and call them from within the implementation block
*/
fn wrapped_sum_query(position: &[i32], tree: &Array<i64, IxDyn>) -> i64 {
    fn query_helper(position: &[i32], tree: &Array<i64, IxDyn>) -> i64 {
        let mut dimension = position[0];
        let mut sum = 0;
        while dimension > 0 {
            if position.len() != 1 {
                sum += query_helper(&position[1..], &tree.index_axis(ndarray::Axis(0), dimension as usize).to_owned());
            } else {
                sum += tree[dimension as usize];
            }
            dimension -= dimension & -dimension;
        }
        return sum;
    }

    query_helper(&position, &tree)
}

fn fill_tree(dim: i32, inp: ArrayView<i64, IxDyn>, position: &mut [i32], tree: &mut NdBIT) {
    let pos_index = position.len() - dim as usize;

    if dim == 1 {
        inp.iter().enumerate().for_each(|(i, &val)| {
            position[pos_index] = i as i32;
            update_helper(position, val, &mut tree.tree.view_mut());
        });
    } else {
        for (i, subview) in inp.axis_iter(ndarray::Axis(0)).enumerate() {
            position[pos_index] = i as i32;
            fill_tree(dim - 1, subview, position, tree);
        }
    }
}


    // Internal helper function that works with slices
fn update_helper(position: &[i32], val: i64, tree: &mut ArrayViewMut<i64, IxDyn>) {
    // Convert from 0-based to 1-based indexing
    let mut dimension = position[0] + 1;
    let len = tree.shape()[0] as i32;
    
    while dimension < len {
        if position.len() > 1 {
            update_helper(
                &position[1..], 
                val, 
                &mut tree.index_axis_mut(ndarray::Axis(0), dimension as usize)
            );
        } else {
            tree[dimension as usize] += val;
        }
        dimension += dimension & -dimension;
    }
}

#[pymethods]
impl NdBIT {
    // takes a python list as input and checks if its a i32 or a list    
    fn update(&mut self, position: Vec<i32>, val: i64) {
        // No need to create a new Vec - just pass the slice directly
        update_helper(&position, val, &mut self.tree.view_mut());
    }

    #[new]
    fn new(input: PyReadonlyArrayDyn<i64>, dim: i32) -> Self {
        
        let inp = input.as_array();

        // 1 index the tree in all dimensions and zero all values
        let tree: Array<i64, IxDyn> = Array::zeros(IxDyn(&inp.shape().iter().map(|x| *x+1 as usize).collect::<Vec<usize>>()));
        let size = inp.len() as i32;
        
        let mut nd_fenwick = NdBIT { tree, dim, size };

        let mut slice: Vec<i32> = vec![0; dim as usize];

        fill_tree(dim, inp, &mut slice, &mut nd_fenwick);

        return nd_fenwick;
    }

    #[getter]
    fn get_tree<'py>(&self, py: Python<'py>) -> Py<PyArray<i64, IxDyn>> {
        self.tree.clone().into_pyarray(py).unbind()
    }
    
    /*
        Calculates the sum of the elements in the range [0, position]
        position is a vector of the same length as the dimension of the tree
     */
    fn sum(&self, position: Vec<i32>) -> i64 {
        let position: Vec<i32> = position.iter().map(|x| x + 1).collect();
        wrapped_sum_query(&position, &self.tree)
    }

    /*
        Calculates the sum of the elements in the range [point1, point2]
        point1 and point2 are vectors of the same length as the dimension of the tree
        The function returns None if the dimensions of the points do not match the dimensions of the tree
        Currently only supports 1D and 2D trees for all other dimensions it will return None
     */
    fn range_sum(&self, start: Vec<i32>, end: Vec<i32>) -> Option<i64> {
        if start.len() != end.len() ||
           start.len() != self.dim as usize || 
           end.len() != self.dim as usize {
            return None;
        }

        match self.dim {
            1 => return Some(self.sum(end) - self.sum(start)),
            2 => {
                let s1 = self.sum(end.clone());
                let s2 = self.sum(vec![end[0], start[1]-1]);
                let s3 = self.sum(vec![start[0]-1, end[1]]);
                let s4 = self.sum(start.into_iter().map(|x| x-1).collect());
                
                return Some(s1 - s2 - s3 + s4);
            },
            _ => {
                return None;
            }
        }
    }
}
