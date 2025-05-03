def too_much_conditions(a: int, b: int) -> int:
    breakpoint()
    if b == 0:
        breakpoint()
        return 1
    if b == 1:
        breakpoint()
        return a ** 1
    if b == 2:
        breakpoint()
        return a ** 2
    if b == 3:
        breakpoint()
        return a ** 3
    if b == 4:
        breakpoint()
        return a ** 4
    breakpoint()
    return a ** 5

for b in range(0, 6):
    too_much_conditions(2, b)
