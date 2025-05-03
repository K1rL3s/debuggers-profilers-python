# Интеграция с Fortran

## Описание
Интеграция Python с Fortran использует f2py (часть NumPy) для создания Python-модулей из Fortran-кода, ускоряя численные вычисления.

## Основные возможности
- Вызов Fortran-функций из Python.
- Создание Python-модулей из Fortran-кода.
- Высокая производительность для научных вычислений.
- Доступ к обширным Fortran-библиотекам.

## Установка
Установите NumPy, включающий f2py:
```
pip install numpy
```
Требуется Fortran-компилятор (например, gfortran).

## Использование
Напишите Fortran-код, скомпилируйте с f2py:
```
f2py -c -m mymodule myscript.f90
```

## Примеры
```fortran
subroutine add(a, b, c)
    integer, intent(in) :: a, b
    integer, intent(out) :: c
    c = a + b
end subroutine add
```
Скомпилируйте и импортируйте в Python.

## Плюсы
- Высокая производительность для численных задач.
- Доступ к существующим Fortran-библиотекам.
- Подходит для научных вычислений.

## Минусы
- Требует знание Fortran.
- Управление двумя языками усложняет проект.

## Ссылки
- [Документация f2py](https://numpy.org/doc/stable/f2py/)
- [Репозиторий GitHub NumPy](https://github.com/numpy/numpy)
