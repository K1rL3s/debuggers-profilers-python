# Windows: gcc -shared -o simple.dll simple.c
# Linux: gcc -shared -o simple.os -fPIC simple.c
import ctypes

# Windows: simple.dll
# Linux: simple.so
lib = ctypes.CDLL('./simple.dll')

lib.add.argtypes = [ctypes.c_int, ctypes.c_int]
lib.add.restype = ctypes.c_int

result = lib.add(5, 3)
print(f"Результат: {result}")  # Результат: 8
