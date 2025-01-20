use pyo3::prelude::*;

/// Formats the sum of two numbers as string.
// #[pyfunction]
// fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
//     Ok((a + b).to_string())
// }

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
// fn main() {
//     let n = 5;

//     let mut tree = FenwickTree::new(n);

//     let sum = tree.sum(3);

//     //dbg!(&tree.tree);

//     println!("Sum of first 4 elements is {}", sum);

//     tree.update(2, 10);

//     let sum = tree.sum(3);

//     // dbg!(&tree.tree);

//     println!("Sum of first 4 elements after update is {}", sum);

// }

// Fenwick tree is represented using a Vector
#[pyclass]
struct FenwickTree {
    tree: Vec<i32>,
}

#[pymethods]
impl FenwickTree {
    // Adds value to the current value at index (this is the update outlined by the geeksforgeeks article)
    fn update(&mut self, mut index: i32, value: i32) {
        // 1 indexed cause that just how it be
        index = index + 1;

        while index <= (self.tree.len()-1) as i32 {
            self.tree[index as usize] += value;
            index += index & (-index);
        }
    }

    // This function behaves more like what you would expect from an update function where it overides the value at index
    // And then propagates the change up the tree. NOTE: Be careful as this may result in negative values in the tree
    // so please exercise caution when using this
    // TODO: add failsafe to prevent negative values
    fn override_update(&mut self, mut index: i32, value: i32) {
        // 1 indexed cause that just how it be
        index = index + 1;

        let diff = value - self.tree[index as usize];

        while index <= (self.tree.len()-1) as i32 {
            self.tree[index as usize] += diff;
            index += index & (-index);
        }
    }

    #[new]
    fn new(size: i32) -> Self {
        let mut tree = vec![0; (size + 1) as usize];
        tree[0] = -9999; // Placeholder for 1-indexed tree
        let mut fenwick_tree = FenwickTree { tree };
        for x in 0..size {
            // dbg!(x);
            fenwick_tree.update(x, x+1);
        }

        return fenwick_tree;
    }

    fn sum(&self, mut index: i32) -> i32 {
        // 1 indexed cause that just how it be
        index = index + 1;
        let mut sum = 0;

        while index > 0 {
            sum += self.tree[index as usize];
            index -= index & -index;
        }

        sum
    }

    // Returns the sum of the elements in the range [left, right]
    fn range_sum(&self, left: i32, right: i32) -> i32 {
        self.sum(right) - self.sum(left - 1)
    }
}
