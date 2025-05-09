import timeit

def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

n = 30
print(timeit.timeit("fib(n)", globals=locals(), number=1000))
# python: 89.13345369999297
# pypy: 11.242766199997277
