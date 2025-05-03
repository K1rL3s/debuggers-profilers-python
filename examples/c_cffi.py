# Windows: gcc -shared -o c_simple.dll c_simple.c
# Linux: gcc -shared -o c_simple.os -fPIC c_simple.c
from cffi import FFI

ffi = FFI()
ffi.cdef("int multiply(int a, int b);")

# Windows: c_simple.dll
# Linux: c_simple.so
lib = ffi.dlopen("c_simple.dll")

result = lib.multiply(4, 5)
print(f"Результат: {result}")  # Результат: 20
