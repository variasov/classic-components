import inspect
from typing import Any

from .types import Class, Method


def add_extra_annotation(method: Method, key: str, value: Any) -> Method:
    """Добавляет дополнительные аннотации к методам.

    >>> def some_func():
    ...     pass
    >>> add_extra_annotation(some_func, 'some_dep', str)
    >>> some_func.__extra_annotations__
    {'some_dep': str}
    """

    if not hasattr(method, '__extra_annotations__'):
        method.__extra_annotations__ = {}

    method.__extra_annotations__[key] = value

    return method


def is_have_extra_annotations(method: Method) -> bool:
    """Предикат, определяющиий, есть ли у метода дополнительные аннотации"""
    return hasattr(method, '__extra_annotations__')


def extra_annotations(cls: Class) -> Class:
    """
    Декоратор для классов, собирающий дополнительные аннотации со всех методов,
    и добавляющий доп. аннотации к аннотациям класса.

    >>> class SomeClass:
    ...
    ...     def some_method(self):
    ...         pass
    ...
    >>> add_extra_annotation(SomeClass.some_method, 'some_dep', str)
    >>> SomeClass = extra_annotations(SomeClass)
    >>> SomeClass.__annotations__
    {'some_dep': str}
    """

    members = inspect.getmembers(cls, is_have_extra_annotations)
    for __, member in members:
        for prop_name, prop_type in member.__extra_annotations__.items():
            cls.__annotations__[prop_name] = prop_type

    return cls
