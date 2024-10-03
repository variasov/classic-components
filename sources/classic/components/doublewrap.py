from functools import wraps


def doublewrap(fn):
    """
    Классный сниппет, облегчающий создание декораторов с параметрами.
    Взято отсюда: https://stackoverflow.com/a/14412901
    В сравнении с оригиналом чуть-чуть улучшена читаемость.

    Пример:

    >>> from classic.components import doublewrap
    ...
    ... @doublewrap
    ... def with_default(method, default):
    ...
    ...     @wraps(method)
    ...     def wrapper(self, *args, **kwargs):
    ...         return method(self, *args, **kwargs) or default
    ...
    ...     return wrapper
    ...
    ... @with_default(1)
    ... def return_none():
    ...     return None
    ...
    ... return_none()
    1
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
