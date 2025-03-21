use ndarray::{Array, ArrayD, IxDyn};
use pyo3::{prelude::*, types::PyList};
use rand::prelude::*;
use numpy::{IntoPyArray, PyArray};
use rayon::prelude::*;

fn ndmatrix_creation(dim: Vec<i32>, random_range: (i32,i32)) -> Array<i32, IxDyn> {
    let mut arr = Array::zeros(dim.iter().map(|&x| x as usize).collect::<Vec<_>>());
     arr.mapv_inplace(|_| rand::random_range(random_range.0..random_range.1));
     arr
 }

 #[pyfunction]
 // Linear function to create a random matrix of any dimension.
 // The matrix is created by recursively creating a matrix of one dimension lower until the base case is reached.
 fn create_random_ndmatrix(py: Python, dim: Vec<i32>, random_range: (i32,i32)) -> Py<PyArray<i32, IxDyn>> {
     let arr = ndmatrix_creation(dim, random_range);
     return arr.into_pyarray(py).unbind();
 }

// This function is the same as the one above, but it uses Rayon to parallelize the creation of the matrix.
// Currently on small inputs it is slower than the sequential version, but on larger inputs it MIGHT be faster.
// This is however untested so the speed is currently unknown. Please just use the sequential version for now.
//TODO: Fix this to use ndArray instead in parrallel build time
#[pyfunction]
fn create_random_ndmatrix_async(dim: Vec<i32>, random_range: (i32, i32)) -> PyResult<PyObject> {
    fn recursion_helper_async(dim: Vec<i32>, random_range: (i32, i32), py: Python) -> Vec<PyObject> { 
        if dim.len() == 1 {
            let temp: Vec<PyObject> = (0..dim[0])
            .map(|_| {
                Python::with_gil(|py| {
                rand::thread_rng().gen_range(random_range.0..random_range.1).into_py(py)
                })
            })
            .collect();
            return temp;
        }
        

        let arr: Vec<PyObject> = py.allow_threads(|| {
            (0..dim[0])
                .into_par_iter()
                .map(|_| {
                    Python::with_gil(|py| {
                        recursion_helper_async(dim[1..].to_vec(), random_range, py).into_py(py)
                    })
                })
                .collect()
        });

        return arr;
    }
    Python::with_gil(|py| Ok(PyList::new(py, recursion_helper_async(dim, random_range, py))?.into()))
}


//A Python module implemented in Rust.
#[pymodule]
fn MatrixGenerator(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(create_random_ndmatrix_async, m)?)?;
    m.add_function(wrap_pyfunction!(create_random_ndmatrix, m)?)?;
    Ok(())
}
