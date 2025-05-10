def max_pair_product(numbers):
    if len(numbers) < 2:
        raise ValueError("Список должен содержать как минимум два элемента")
    max_product = float('-inf')
    for i in range(len(numbers) - 1):
        product = numbers[i] * numbers[i + 1]
        if product > max_product:
            max_product = product
    return max_product

print(max_pair_product([3, 6, -2, 7, 4]))  # Должен вернуть 28 (7 * 4)
print(max_pair_product([5]))  # Должен вернуть ошибку
print(max_pair_product([]))  # Должен вернуть ошибку

