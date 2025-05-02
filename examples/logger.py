import logging

logger = logging.getLogger(__name__)

logging.basicConfig(
    filemode="a",
    format="%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
    datefmt="%H:%M:%S",
    style="%",
    level=logging.DEBUG,
)

tralalelo = "tralala"
bombordiro = "crocodilo"
brr_brr = "patapim"

logger.debug("%s %s %s", tralalelo, bombordiro, brr_brr)
logger.info("%s---%s---%s", tralalelo, bombordiro, brr_brr)
logger.warning("%s, %s, %s", tralalelo, bombordiro, brr_brr)
"""
00:51:35 - [DEBUG] -  __main__ - (logger.py).<module>(17) - tralala crocodilo patapim
00:51:35 - [INFO] -  __main__ - (logger.py).<module>(18) - tralala---crocodilo---patapim
00:51:35 - [WARNING] -  __main__ - (logger.py).<module>(19) - tralala, crocodilo, patapim
"""


def calculator(a: int, b: int, operation: str) -> int | None:
    logger.debug("Переданные значения: a=%d, b=%d, operation=%s", a, b, operation)

    if operation == "+":
        logger.debug("Складываю %d и %d", a, b)
        logger.debug("Результат: %d\n", a + b)
        return a + b
    if operation == "-":
        logger.debug("Вычитаю из %d число %d", a, b)
        logger.debug("Результат: %d\n", a - b)
        return a - b
    if operation == "*":
        logger.debug("Умножаю %d и %d", a, b)
        logger.debug("Результат: %d\n", a * b)
        return a * b

    logger.warning("Не нашёл подходящее действия для оператора %s возвращаю None", operation)
    return None


calculator(1, 2, "+")
calculator(3, 4, "-")
calculator(5, 6, "*")
calculator(7, 8, "/")

"""
00:51:35 - [DEBUG] -  __main__ - (logger.py).calculator(26) - Переданные значения: a=1, b=2, operation=+
00:51:35 - [DEBUG] -  __main__ - (logger.py).calculator(29) - Складываю 1 и 2
00:51:35 - [DEBUG] -  __main__ - (logger.py).calculator(30) - Результат: 3

00:51:35 - [DEBUG] -  __main__ - (logger.py).calculator(26) - Переданные значения: a=3, b=4, operation=-
00:51:35 - [DEBUG] -  __main__ - (logger.py).calculator(33) - Вычитаю из 3 число 4
00:51:35 - [DEBUG] -  __main__ - (logger.py).calculator(34) - Результат: -1

00:51:35 - [DEBUG] -  __main__ - (logger.py).calculator(26) - Переданные значения: a=5, b=6, operation=*
00:51:35 - [DEBUG] -  __main__ - (logger.py).calculator(37) - Умножаю 5 и 6
00:51:35 - [DEBUG] -  __main__ - (logger.py).calculator(38) - Результат: 30

00:51:35 - [DEBUG] -  __main__ - (logger.py).calculator(26) - Переданные значения: a=7, b=8, operation=/
00:51:35 - [WARNING] -  __main__ - (logger.py).calculator(41) - Не нашёл подходящее действия для оператора / возвращаю None
"""