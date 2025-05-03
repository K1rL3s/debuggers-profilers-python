use pyo3::prelude::*;
use uuid::Uuid;
use pyo3::exceptions::PyOSError;
use pyo3::wrap_pyfunction;
use pyo3_log;

#[pyfunction]
fn generate_uuid4() -> PyResult<String> {
    Ok(Uuid::new_v4())?.to_string()
}

#[pymodule]
fn rust_uuid(_py: Python, m: &PyModule) -> PyResult<()> {
    pyo3_log::init();
    m.add_function(wrap_pyfunction!(generate_uuid4))?;
    Ok(())
}