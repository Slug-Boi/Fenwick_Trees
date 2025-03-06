use pyo3::{ffi::PyNumberMethods, prelude::*, types::{PyInt, PyList, PyString}};
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

// This is an n-dimensional fenwick tree that is used to store the sum of elements in a n-dimensional array
// The tree is the nested arrays that store the sum of elements
// The tree is 1 indexed in all dimensions
// dimensions is the number of dimensions of the tree
// The size is a vector of the n-th dimension sizes
#[pyclass]
struct NdFenwick {
    tree: Vec<PyObject>,
    dim: i32,
    size: Vec<i32>
}

#[pymethods]
impl NdFenwick {
    
    // takes a python list as input and checks if its a i32 or a list
    fn create_empty_bit(&self, dim: i32, inp: Bound<'_,PyList>) -> Vec<PyObject> {
        Python::with_gil(|py| {
            if dim == 1 {
                // return the all 0 vec
                return (0..inp.len()).map(|_| 0.into_py(py)).collect();
            }
            let mut bit = Vec::new();
            for i in 0..inp.len() {
                let val = inp.get_item(i);
                match val {
                    Ok(val) => {
                        if val.is_instance_of::<PyList>() {
                            bit.extend(self.create_empty_bit(dim-1, val.downcast::<PyList>().unwrap().clone()));
                        } 
                    }
                    Err(e) => {
                        println!("Error: {}", e);
                    }
                }
            }
            bit.into_iter().map(|x| x.into_py(py)).collect::<Vec<PyObject>>()
        })
    }

    fn FillTree(&mut self, inp: Bound<'_, PyList>, dim: i32, position: Bound<'_, PyList>) {
        Python::with_gil(|py| {
        if dim == 1 {
            for i in 0..inp.len() {
                let mut temp_pos = position.clone();
                temp_pos.append(i.into_py(py)).unwrap();
                let temp_pos_vec: Vec<i32> = temp_pos.iter().map(|x| x.extract::<i32>().unwrap()).collect();
                self.Update(temp_pos_vec, inp.get_item(i).unwrap().extract::<i32>().unwrap());
            }
            return;
        }

        for i in 0..inp.len() {
            let mut temp_pos = position.clone();
            temp_pos.append(i.into_py(py)).unwrap();
            self.FillTree(inp.get_item(i).unwrap().downcast::<PyList>().unwrap().clone(), dim-1, temp_pos);
        }
        });
    }

    fn Update(&mut self, position: Vec<i32>, val: i32) {
        fn UpdateHelper(position: &[i32], val: i32, array: &mut Vec<PyObject>) {
            Python::with_gil(|py| {
            let mut dimension = position[0] as usize;
            while dimension < array.len() {
                if position.len() != 1 {
                    UpdateHelper(&position[1..], val, array[dimension].extract::<Vec<PyObject>>(py).unwrap().as_mut());
                } else {
                    array[dimension] = (array[dimension].extract::<i32>(py).unwrap() + val).into_py(py);
                }
                dimension += dimension & -(dimension as i32) as usize;
            }
            });
        }

        let position: Vec<i32> = position.iter().map(|x| x + 1).collect();
        
        UpdateHelper(&position, val, &mut self.tree);
    }

    #[new]
    fn new(input: Bound<'_, PyList>, dim: i32) -> Self {
        let mut size = Vec::new();
        size.push(input.len() as i32);
        let mut instance = NdFenwick { tree: Vec::new(), dim, size: Vec::new() };
        instance.create_empty_bit(dim, input.clone());
        Python::with_gil(|py| {
            instance.FillTree(input, dim, PyList::empty(py));
        });


        return instance;
    }

    fn get_tree(&self) -> &Vec<PyObject> {
        &self.tree
    }

}
