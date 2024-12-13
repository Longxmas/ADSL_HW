from concurrent.futures import ThreadPoolExecutor
def compute(x):
    x = x * 2
    return x
result = list(ThreadPoolExecutor().map(compute, [1, 2, 3]))
