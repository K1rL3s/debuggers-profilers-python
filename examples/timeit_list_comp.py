import timeit

n = 1_000_000

print(
    timeit.timeit("list(map(str, r))",
    setup="r=range(100)", number=n)
)
# 7.257156100000429

print(
    timeit.timeit("[str(x) for x in r]",
    setup="r=range(100)", number=n)
)
# 6.102027400000225

print(
    timeit.timeit("list(map(lambda x: x * 2, r))",
    setup="r=range(100)", number=n)
)
# 4.217808600002172

print(
    timeit.timeit("[x * 2 for x in r]",
    setup="r=range(100)", number=n)
)
# 1.9810508999980811

"""
python -m timeit --number=1_000_000 --setup="r=range(100)" "list(map(str, r))"
1000000 loops, best of 5: 6.24 usec per loop

python -m timeit --number=1_000_000 --setup="r=range(100)" "[str(x) for x in r]"
1000000 loops, best of 5: 5.24 usec per loop

python -m timeit --number=1_000_000 --setup="r=range(100)" "list(map(lambda x: x * 2, r))"
1000000 loops, best of 5: 4.23 usec per loop

python -m timeit --number=1_000_000 --setup="r=range(100)" "[x * 2 for x in r]"
1000000 loops, best of 5: 1.98 usec per loop
"""
