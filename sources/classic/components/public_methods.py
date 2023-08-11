import inspect
from typing import Iterable, Tuple

from .types import Class, Decorators, Method


def wrap_public_methods(cls: Class, decorators: Decorators) -> Class:
    """Декоратор для классов, позволяющий обернуть каждый публичный метод класса
    в указанные декораторы.

    >>> def some_decorator(func):
    ...     def wrapper(*args, **kwargs):
    ...         print('Start')
    ...         return func(*args, **kwargs)
    ...
    ...     return func
    ...
    >>> @wrap_public_methods([some_decorator])
    ... class SomeClass:
    ...
    ...     def public_method(self):
    ...         pass
    ...
    ...     # Не будет обернуто
    ...     def _protected_method(self):
    ...         pass
    ...
    >>> SomeClass().public_method()
    Start

    """

    if not decorators:
        return cls

    public_methods: Iterable[Tuple[str, Method]] = (
        (name, method)
        for name, method in inspect.getmembers(cls, callable)
        if not name.startswith('_')
    )

    for name, method in public_methods:
        for decorator in decorators:
            method = decorator(method)

        setattr(cls, name, method)

    return cls
