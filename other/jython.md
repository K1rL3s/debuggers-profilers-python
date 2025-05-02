# Jython

## Описание
Jython - это реализация Python, работающая на Java Virtual Machine (JVM). Она позволяет запускать Python-код в Java-среде, обеспечивая доступ к Java-библиотекам.

## Основные возможности
- Выполнение Python-кода на JVM.
- Импорт и использование Java-классов в Python.
- Компиляция Python в байт-код Java.
- Поддержка Java GUI-библиотек (AWT, Swing, SWT).
- Встраивание Python-скриптов в Java-приложения.

## Установка
Jython доступен для загрузки на [официальном сайте](https://www.jython.org/). Следуйте инструкциям для установки на вашей платформе.

## Основное использование
Запустите Python-скрипт с Jython:
```
jython myscript.py
```
Импортируйте Java-классы в Python-коде.

## Пример
```python
from java.util import ArrayList

list = ArrayList()
list.add("Hello")
print(list)
```
Этот код создает Java-список и работает через Jython.

## Плюсы
- Бесшовная интеграция с Java-экосистемой.
- Платформонезависимость благодаря JVM.
- Подходит для встраивания скриптов в Java-приложения.

## Минусы
- Jython 2.7.x поддерживает только Python 2 (Jython 3 в разработке).
- Некоторые Python-библиотеки несовместимы.
- Производительность ниже CPython для чистого Python-кода.

## Ссылки
- [Официальный сайт Jython](https://www.jython.org/)
- [Документация Jython](https://www.jython.org/docs/)
- [Репозиторий GitHub Jython](https://github.com/jython/jython)