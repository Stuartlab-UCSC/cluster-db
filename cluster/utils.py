from decorator import decorator
import time


@decorator
def timeit(func, id_string="", *args, **kwargs):
    ts = time.time()
    result = func(*args, **kwargs)
    te = time.time()
    print('%s  %2.2f ms' % (id_string, (te - ts) * 1000))
    return result
