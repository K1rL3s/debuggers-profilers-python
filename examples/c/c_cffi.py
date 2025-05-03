# Windows: gcc -shared -o simple.dll simple.c
# Linux: gcc -shared -o simple.os -fPIC simple.c
from cffi import FFI

ffi = FFI()
ffi.cdef("int multiply(int a, int b);")

# Windows: simple.dll
# Linux: simple.so
lib = ffi.dlopen("simple.dll")

result = lib.multiply(4, 5)
print(f"Результат: {result}")  # Результат: 20
