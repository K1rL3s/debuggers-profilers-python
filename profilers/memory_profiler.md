# memory_profiler

## Описание
`memory_profiler` - сторонний модуль для мониторинга потребления памяти Python-программ. Он отслеживает использование памяти построчно, помогая выявить утечки и оптимизировать код.

## Основные возможности
- Построчный анализ потребления памяти.
- Декоратор `@profile` для профилирования функций.
- Поддержка отчетов о максимальном использовании памяти.
- Интеграция с `psutil` для точных измерений.

## Установка
Установите через pip:
```
pip install memory_profiler
```

## Основное использование
Добавьте декоратор `@profile`:
```python
@profile
def my_function():
    pass
```
Запустите:
```
python -m memory_profiler script.py
```

## Пример
```python
from memory_profiler import profile

@profile
def create_list(n):
    lst = [i for i in range(n)]
    return lst

create_list(1000000)
```
Запустите для получения отчета о памяти.

## Плюсы
- Выявляет участки кода с высоким потреблением памяти.
- Полезен для обнаружения утечек памяти.

## Минусы
- Требует установки стороннего пакета.
- Может замедлять выполнение из-за мониторинга памяти.

## Ссылки
- [GitHub memory_profiler](https://github.com/pythonprofilers/memory_profiler)
- [PyPI memory-profiler](https://pypi.org/project/memory-profiler/)