use pyo3::prelude::*;
use numpy::PyReadonlyArrayDyn;
use ndarray::{prelude::*, ViewRepr};

#[pyfunction]
fn linear_matrix_sum(input: PyReadonlyArrayDyn<i64>, start: Vec<i32>, end: Vec<i32> ) -> i64 {
    let inp = input.as_array();
    
    sum_helper(&start, &end, inp)
}

fn sum_helper(position1: &[i32], position2: &[i32], array: ArrayViewD<i64>) -> i64 {
    // Convert negative indices to positive (Python-style)
    let dim = position1.len();
    let mut start = Vec::with_capacity(dim);
    let mut end = Vec::with_capacity(dim);
    
    for (i, (&s, &e)) in position1.iter().zip(position2.iter()).enumerate() {
        let dim_size = array.shape()[i] as i32;
        let s = if s < 0 { dim_size + s } else { s };
        let e = if e < 0 { dim_size + e } else { e };
        
        if s < 0 || e >= dim_size || s > e {
            panic!("Invalid bounds for dimension {}: start={}, end={}", i, s, e);
        }
        
        start.push(s as usize);
        end.push(e as usize);
    }
    
    let mut sum = 0;
    
    if dim == 1 {
        // Base case: 1D array
        for i in start[0]..=end[0] {
            sum += array[[i]];
        }
    } else {
        // Recursive case: nD array
        for i in start[0]..=end[0] {
            let sub_array = array.index_axis(ndarray::Axis(0), i);
            sum += sum_helper(&position1[1..], &position2[1..], sub_array);
        }
    }
    
    sum
}
    

#[pymodule]
fn MatrixSummer(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(linear_matrix_sum, m)?)?;
    Ok(())
}
