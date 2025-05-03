use pyo3::prelude::*;
use uuid::Uuid;

#[pyfunction]
fn generate_uuid4() -> String {
    Uuid::new_v4().to_string()
}

#[pymodule]
fn rust_uuid(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(generate_uuid4, m)?)?;
    Ok(())
}
