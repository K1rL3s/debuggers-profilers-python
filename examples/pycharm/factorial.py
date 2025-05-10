def factorial(n):
    if n < 0:
        raise ValueError("Факториал не определен для отрицательных чисел")
    if n == 0:
        return 1
    return n * factorial(n - 1)

print(factorial(-1))  # Теперь вызовет ValueError


