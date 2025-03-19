use pyo3::{prelude::*, types::PyList};
use rand::prelude::*;
use rayon::prelude::*;


#[pyfunction]
fn create_random_ndmatrix(dim: Vec<i32>, random_range: (i32, i32)) -> PyResult<PyObject> {
    fn recursion_helper(dim: Vec<i32>, random_range: (i32, i32), py: Python) -> PyResult<PyObject> { 
        if dim.len() == 1 {
            let temp: Vec<PyObject> = (0..dim[0])
                .map(|_| rand::random_range(random_range.0..random_range.1).into_py(py))
                .collect();
            return Ok(PyList::new(py, temp)?.into());
        }
    
        let arr: Vec<PyObject> = (0..dim[0])
            .map(|_| recursion_helper(dim[1..].to_vec(), random_range, py).unwrap().into_py(py))
            .collect();
        return Ok(PyList::new(py, arr)?.into());
    }
    Python::with_gil(|py| recursion_helper(dim, random_range, py))
}

// This function is the same as the one above, but it uses Rayon to parallelize the creation of the matrix.
// Currently on small inputs it is slower than the sequential version, but on larger inputs it MIGHT be faster.
// This is however untested so the speed is currently unknown. Please just use the sequential version for now.
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
