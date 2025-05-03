#include <Python.h>

static PyObject* add_numbers(PyObject* self, PyObject* args) {
    int a, b;
    if (!PyArg_ParseTuple(args, "ii", &a, &b)) {
        return NULL;
    }
    return Py_BuildValue("i", a + b);
}

static PyMethodDef integration_methods[] = {
    {"add_numbers", add_numbers, METH_VARARGS, "Add two numbers."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef integration_module = {
    PyModuleDef_HEAD_INIT,
    "integration",
    "A module to add numbers.",
    -1,
    integration_methods
};

#ifdef _WIN32
__declspec(dllexport)
#endif
PyMODINIT_FUNC PyInit_integration(void) {
    return PyModule_Create(&integration_module);
}