import time
import timeit
import uuid
import rust_uuid

def measure_time(func, iterations):
    start = time.time()
    for _ in range(iterations):
        func()
    return time.time() - start

n = 1_000_000

python_uuid4 = timeit.timeit("str(uuid.uuid4())", number=n, globals=locals())
print(f"Python uuid4: {python_uuid4}")

rust_uuid4 = timeit.timeit("rust_uuid.generate_uuid4", number=n, globals=locals())
print(f"Rust uuid4: {python_uuid4}")
