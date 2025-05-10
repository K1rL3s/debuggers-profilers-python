from memory_profiler import profile

@profile
def main():
    n = 100_000_000
    a = tuple(range(n))
    b = list(range(n))
    del a
    del b

main()