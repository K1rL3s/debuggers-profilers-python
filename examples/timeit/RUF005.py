import timeit

small_list_a = list(range(10))
small_list_b = list(range(10, 20))
small_list_c = list(range(20, 30))

def plus_small_lists():
    return small_list_a + small_list_b + small_list_c

def unpack_small_lists():
    return [*small_list_a, *small_list_b, *small_list_c]

medium_list_a = list(range(1_000))
medium_list_b = list(range(1_000, 2_000))
medium_list_c = list(range(2_000, 3_000))

def plus_medium_lists():
    return medium_list_a + medium_list_b + medium_list_c

def unpack_medium_lists():
    return [*medium_list_a, *medium_list_b, *medium_list_c]

large_list_a = list(range(100_000))
large_list_b = list(range(100_000, 200_000))
large_list_c = list(range(200_000, 300_000))

def plus_large_lists():
    return large_list_a + large_list_b + large_list_c

def unpack_large_lists():
    return [*large_list_a, *large_list_b, *large_list_c]

small_tuple_a = tuple(range(10))
small_tuple_b = tuple(range(10, 20))
small_tuple_c = tuple(range(20, 30))

def plus_small_tuples():
    return small_tuple_a + small_tuple_b + small_tuple_c

def unpack_small_tuples():
    return (*small_tuple_a, *small_tuple_b, *small_tuple_c)

medium_tuple_a = tuple(range(1_000))
medium_tuple_b = tuple(range(1_000, 2_000))
medium_tuple_c = tuple(range(2_000, 3_000))

def plus_medium_tuples():
    return medium_tuple_a + medium_tuple_b + medium_tuple_c

def unpack_medium_tuples():
    return (*medium_tuple_a, *medium_tuple_b, *medium_tuple_c)

large_tuple_a = tuple(range(100_000))
large_tuple_b = tuple(range(-100_000, 0, 2))
large_tuple_c = tuple(range(100_000, 200_000))

def plus_large_tuples():
    return large_tuple_a + large_tuple_b + large_tuple_c

def unpack_large_tuples():
    return (*large_tuple_a, *large_tuple_b, *large_tuple_c)

small_set_a = set(range(10))
small_set_b = set(range(5, 15))
small_set_c = set(range(10, 20))

def plus_small_sets():
    return small_set_a | small_set_b | small_set_c

def unpack_small_sets():
    return {*small_set_a, *small_set_b, *small_set_c}

medium_set_a = set(range(1_000))
medium_set_b = set(range(500, 1_500))
medium_set_c = set(range(1_000, 2_000))

def plus_medium_sets():
    return medium_set_a | medium_set_b | medium_set_c

def unpack_medium_sets():
    return {*medium_set_a, *medium_set_b, *medium_set_c}

large_set_a = set(range(100_000))
large_set_b = set(range(50_000, 150_000))
large_set_c = set(range(100_000, 200_000))

def plus_large_sets():
    return large_set_a | large_set_b | large_set_c

def unpack_large_sets():
    return {*large_set_a, *large_set_b, *large_set_c}

small_str_a = "a" * 10
small_str_b = "b" * 10
small_str_c = "c" * 10

def plus_small_strings():
    return small_str_a + small_str_b + small_str_c

def unpack_small_strings():
    return "".join([small_str_a, small_str_b, small_str_c])

medium_str_a = "a" * 1_000
medium_str_b = "b" * 1_000
medium_str_c = "c" * 1_000

def plus_medium_strings():
    return medium_str_a + medium_str_b + medium_str_c

def unpack_medium_strings():
    return "".join([medium_str_a, medium_str_b, medium_str_c])

large_str_a = "a" * 100_000
large_str_b = "b" * 100_000
large_str_c = "c" * 100_000

def plus_large_strings():
    return large_str_a + large_str_b + large_str_c

def unpack_large_strings():
    return "".join([large_str_a, large_str_b, large_str_c])

n = 10_000

print("Small Lists:")
print("Plus:", timeit.timeit(plus_small_lists, number=n))
print("Unpack:", timeit.timeit(unpack_small_lists, number=n))

print("\nMedium Lists:")
print("Plus:", timeit.timeit(plus_medium_lists, number=n))
print("Unpack:", timeit.timeit(unpack_medium_lists, number=n))

print("\nLarge Lists:")
print("Plus:", timeit.timeit(plus_large_lists, number=n))
print("Unpack:", timeit.timeit(unpack_large_lists, number=n))

print("\nSmall Tuples:")
print("Plus:", timeit.timeit(plus_small_tuples, number=n))
print("Unpack:", timeit.timeit(unpack_small_tuples, number=n))

print("\nMedium Tuples:")
print("Plus:", timeit.timeit(plus_medium_tuples, number=n))
print("Unpack:", timeit.timeit(unpack_medium_tuples, number=n))

print("\nLarge Tuples:")
print("Plus:", timeit.timeit(plus_large_tuples, number=n))
print("Unpack:", timeit.timeit(unpack_large_tuples, number=n))

print("\nSmall Sets:")
print("Plus (|):", timeit.timeit(plus_small_sets, number=n))
print("Unpack:", timeit.timeit(unpack_small_sets, number=n))

print("\nMedium Sets:")
print("Plus (|):", timeit.timeit(plus_medium_sets, number=n))
print("Unpack:", timeit.timeit(unpack_medium_sets, number=n))

print("\nLarge Sets:")
print("Plus (|):", timeit.timeit(plus_large_sets, number=n))
print("Unpack:", timeit.timeit(unpack_large_sets, number=n))

print("\nSmall Strings:")
print("Plus:", timeit.timeit(plus_small_strings, number=n))
print("Unpack (join):", timeit.timeit(unpack_small_strings, number=n))

print("\nMedium Strings:")
print("Plus:", timeit.timeit(plus_medium_strings, number=n))
print("Unpack (join):", timeit.timeit(unpack_medium_strings, number=n))

print("\nLarge Strings:")
print("Plus:", timeit.timeit(plus_large_strings, number=n))
print("Unpack (join):", timeit.timeit(unpack_large_strings, number=n))

"""
Small Lists:
Plus: 0.0014413999997486826
Unpack: 0.0011602000013226643

Medium Lists:
Plus: 0.09322900000188383
Unpack: 0.06581910000022617

Large Lists:
Plus: 28.674024500000087
Unpack: 21.940253500000836

Small Tuples:
Plus: 0.0014080000000831205
Unpack: 0.0017112000023189466

Medium Tuples:
Plus: 0.09390469999925699
Unpack: 0.1142760000002454

Large Tuples:
Plus: 22.971861699999863
Unpack: 36.24664879999909

Small Sets:
Plus (|): 0.005046599999332102
Unpack: 0.002942399998573819

Medium Sets:
Plus (|): 0.45124659999783034
Unpack: 0.30211010000130045

Large Sets:
Plus (|): 99.91852979999749
Unpack: 68.54525009999998

Small Strings:
Plus: 0.0007353000000875909
Unpack (join): 0.0008352999975613784

Medium Strings:
Plus: 0.0021503000025404617
Unpack (join): 0.0013703000004170462

Large Strings:
Plus: 0.10228190000270843
Unpack (join): 0.06090970000150264
"""