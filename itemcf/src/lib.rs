use pyo3::prelude::*;

#[pyfunction]
fn foo() -> i32 {
    100
}

#[pymodule]
fn itemcf(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(foo, m)?)?;

    Ok(())
}
