cdef extern from "simple.h":
    int add(int a, int b)
    int multiply(int a, int b)


cdef int subtract(int a, int b):
    return a - b


def py_add(int a, int b) -> int:
    return add(a, b)

def py_multiply(int a, int b) -> int:
    return multiply(a, b)

def py_subtract(int a, int b) -> int:
    return subtract(a, b)
