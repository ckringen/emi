from memory_profiler import profile

def add3(n):
    return n + 3
add3 = profile(add3)

print(add3(3))
