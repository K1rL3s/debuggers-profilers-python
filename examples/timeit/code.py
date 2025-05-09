import timeit

print(timeit.timeit("list(map(str, r))", setup="r=range(100)"))
# 7.257156100000429
print(timeit.timeit("[str(x) for x in r]", setup="r=range(100)"))
# 6.102027400000225