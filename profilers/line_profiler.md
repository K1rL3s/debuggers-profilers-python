# line_profiler

## Описание
`line_profiler` - сторонний инструмент для построчного профилирования Python-кода. Он показывает время, затраченное на каждую строку функции, что помогает выявить точные узкие места.

## Основные возможности
- Построчное измерение времени выполнения кода.
- Использование декоратора `@profile` для выбора функций.
- Подробные отчеты с процентом времени на каждую строку.
- Интеграция с инструментами, такими как [Spyder](https://www.spyder-ide.org/).

## Установка
Установите через pip:
```
pip install line_profiler
```

## Использование
Добавьте декоратор `@profile` к функции:
```python
@profile
def my_function():
    pass
```
Запустите с `kernprof`:
```
kernprof -l script.py
```
Просмотрите результаты:
```
python -m line_profiler script.py.lprof
```

## Примеры
```python
from line_profiler import profile

@profile
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

fibonacci(10)
```
Запустите с `kernprof` для получения построчной статистики.

## Плюсы
- Детальный анализ времени выполнения строк.
- Простота выбора функций для профилирования.

## Минусы
- Требует установки и настройки.
- Накладные расходы выше, чем у `cProfile`.

## Ссылки
- [GitHub line_profiler](https://github.com/pyutils/line_profiler)
- [PyPI line-profiler](https://pypi.org/project/line-profiler/)