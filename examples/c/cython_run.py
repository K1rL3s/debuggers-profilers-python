import cython_file

result_add = cython_file.py_add(5, 3)
print(f"Сложение: 5 + 3 = {result_add}")

result_multiply = cython_file.py_multiply(4, 5)
print(f"Умножение: 4 * 5 = {result_multiply}")

result_substract = cython_file.py_subtract(10, 5)
print(f"Разность: 10 - 5 = {result_multiply}")
