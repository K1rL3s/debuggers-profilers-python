# Windows: gcc -shared -o c_simple.dll c_simple.c
# Linux: gcc -shared -o c_simple.os -fPIC c_simple.c
import ctypes

# Windows: c_simple.dll
# Linux: c_simple.so
lib = ctypes.CDLL('./c_simple.dll')

lib.add.argtypes = [ctypes.c_int, ctypes.c_int]
lib.add.restype = ctypes.c_int

result = lib.add(5, 3)
print(f"Результат: {result}")  # Результат: 8
