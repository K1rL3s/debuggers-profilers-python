# python capi_setup.py build_ext --inplace --compiler=mingw32
import integration  # Собственный модуль, скомпилированный через Python/C API

result = integration.add_numbers(5, 3)
print(result)  # Вывод: 8
