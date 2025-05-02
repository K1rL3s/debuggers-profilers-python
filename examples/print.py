tralalelo = "tralala"
bombordiro = "crocodilo"
brr_brr = "patapim"

print(tralalelo, bombordiro, brr_brr)  # Вывод: tralala crocodilo patapim
print(tralalelo, bombordiro, brr_brr, sep="---")  # Вывод: tralala---crocodilo---patapim
print(tralalelo, bombordiro, brr_brr, sep=", ")  # Вывод: tralala, crocodilo, patapim

print(tralalelo, end=", ")
print(bombordiro, end=", ")
print(brr_brr)
# Вывод: tralala, crocodilo, patapim

with open("temp.txt", "w") as f:
    print(tralalelo, bombordiro, brr_brr, sep=" | ", end=" = frigo camelo", file=f, flush=True)
# Содержимое файла temp.txt: tralala | crocodilo | patapim = frigo camelo


def calculator(a: float, b: float, operation: str) -> float | None:
    print("Переданные значения: a=", a, ", b=", b, ", operation=", operation, sep="")

    if operation == "+":
        print("Складываю", a, "и", b)
        print("Результат:", a + b, end="\n\n")
        return a + b
    if operation == "-":
        print("Вычитаю из", a, "число", b)
        print("Результат:", a - b, end="\n\n")
        return a - b
    if operation == "*":
        print("Умножаю", a, "и", b)
        print("Результат:", a * b, end="\n\n")
        return a * b

    print("Не нашёл подходящее действия для оператора", operation, "возвращаю None", end="\n\n")
    return None


calculator(1, 2, "+")
calculator(3, 4, "-")
calculator(5, 6, "*")
calculator(7, 8, "/")

"""
Переданные значения: a=1, b=2, operation=+
Складываю 1 и 2
Результат: 3

Переданные значения: a=3, b=4, operation=-
Вычитаю из 3 число 4
Результат: -1

Переданные значения: a=5, b=6, operation=*
Умножаю 5 и 6
Результат: 30

Переданные значения: a=7, b=8, operation=/
Не нашёл подходящее действия для оператора / возвращаю None
"""