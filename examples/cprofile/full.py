import cProfile
import sys
import math

sys.setrecursionlimit(1_000_000)

def recursive_factorial(n: int) -> int:
    if n == 0:
        return 1
    return n * recursive_factorial(n - 1)

def loop_factorial(n: int) -> int:
    factorial = 1
    for i in range(1, n + 1):
        factorial *= i
    return factorial

cProfile.run('recursive_factorial(300_000)')
cProfile.run('loop_factorial(300_000)')
cProfile.run('math.factorial(300_000)')

"""
         300004 function calls (4 primitive calls) in 27.304 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000   27.304   27.304 <string>:1(<module>)
 300001/1   27.304    0.000   27.304   27.304 cprofile.py:9(recursive_factorial)
        1    0.000    0.000   27.304   27.304 {built-in method builtins.exec}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
"""
"""
         4 function calls in 26.556 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000   26.556   26.556 <string>:1(<module>)
        1   26.556   26.556   26.556   26.556 cprofile.py:15(loop_factorial)
        1    0.000    0.000   26.556   26.556 {built-in method builtins.exec}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
"""
"""
         4 function calls in 0.808 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.808    0.808 <string>:1(<module>)
        1    0.000    0.000    0.808    0.808 {built-in method builtins.exec}
        1    0.808    0.808    0.808    0.808 {built-in method math.factorial}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
"""
