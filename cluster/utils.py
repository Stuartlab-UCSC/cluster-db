from decorator import decorator
import datetime, time
from flask_user import current_user


@decorator
def timeit(func, id_string="", *args, **kwargs):
    ts = time.time()
    result = func(*args, **kwargs)
    te = time.time()
    user = 'anonymous user'
    if current_user.is_authenticated:
        user = current_user.email
    print('%s  %s  %s  %2.2f ms' \
        % (datetime.datetime.now(), user, id_string, (te - ts) * 1000))
    return result
