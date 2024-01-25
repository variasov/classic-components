from functools import wraps


def doublewrap(fn):
    """
    Классный сниппет, облегчающий создание декораторов с параметрами.
    Взято отсюда: https://stackoverflow.com/a/14412901
    В сравнении с оригиналом чуть-чуть улучшена читаемость.
    """

    @wraps(fn)
    def new_dec(*args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            # actual decorated function
            return fn(args[0])
        else:
            # decorator arguments
            return lambda real_fn: fn(real_fn, *args, **kwargs)

    return new_dec
