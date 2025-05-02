# pylint

## Описание
`pylint` — это статический анализатор кода для Python (версии 2 и 3, поддерживает Python 3.9.0 и выше). Он проверяет код на наличие ошибок, обеспечивает соблюдение стандартов кодирования (например, PEP 8), выявляет "запахи кода" (code smells) и предлагает рекомендации по рефакторингу без необходимости запуска программы.

## Основные возможности
- **Инференс**: Использует библиотеку `astroid` для вывода фактических значений, что позволяет, например, различать вызовы `logging` и `argparse`.
- **Конфигурируемость**: Поддерживает настройку через файлы конфигурации и плагины (например, `pylint-django`).
- **Дополнительные инструменты**: Включает `pyreverse` для создания UML-диаграмм и `symilar` для поиска похожих функций.
- **Проверка орфографии**: Опциональная проверка с использованием библиотеки `enchant`.

## Установка
Установите с помощью команды:
```
pip install pylint
```
Для проверки орфографии дополнительно установите:
```
pip install pylint[spelling]
```
Это требует наличия библиотеки `enchant` C ([Установка enchant](https://pyenchant.github.io/pyenchant/install.html#installing-the-enchant-c-library)). Pylint интегрируется с большинством редакторов и IDE.

## Основное использование
Запустите `pylint` на файле или директории:
```
pylint myscript.py
```
Для начального анализа используйте флаг `--errors-only`. Отключите определенные категории сообщений с помощью `--disable=C,R` (конвенции и рефакторинг).

## Пример
```bash
pylint --errors-only myscript.py
```
Этот пример запускает `pylint` только для выявления ошибок, игнорируя предупреждения о стиле.

## Плюсы
- Тщательный анализ благодаря инференсу.
- Поддержка стандартной библиотеки Python без дополнительных настроек.
- Широкая экосистема плагинов для специфических задач.
- Дополнительные инструменты, такие как `pyreverse` и `symilar`.

## Минусы
- Медленная работа из-за глубокого анализа.
- Может выдавать предупреждения о намеренно написанном коде.
- Для сторонних библиотек могут потребоваться плагины.

## Ссылки
- [GitHub pylint](https://github.com/pylint-dev/pylint)
- [Документация pylint](https://pylint.readthedocs.io/)
- [PyPI pylint](https://pypi.python.org/pypi/pylint)
- [Установка enchant](https://pyenchant.github.io/pyenchant/install.html#installing-the-enchant-c-library)
- [Плагин pylint-pydantic](https://pypi.org/project/pylint-pydantic)
- [Плагин pylint-django](https://github.com/pylint-dev/pylint-django)
- [Плагин pylint-sonarjson](https://github.com/cnescatlab/pylint-sonarjson-catlab)
- [Сотрудничество с pylint](https://pylint.readthedocs.io/en/latest/development_guide/contribute.html)
- [Кодекс поведения pylint](https://github.com/pylint-dev/pylint/blob/main/CODE_OF_CONDUCT.md)
- [Контакт и поддержка pylint](https://pylint.readthedocs.io/en/latest/contact.html)
- [Tidelift для pylint](https://tidelift.com/subscription/pkg/pypi-pylint?utm_source=pypi-pylint&utm_medium=referral&utm_campaign=readme)
- [Значок pylint](https://pylint.readthedocs.io/en/latest/user_guide/installation/badge.html)

