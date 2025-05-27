from dataclasses import dataclass, field
from typing import Callable, TypeVar

from .types import Class


def auto_init(cls: Class) -> Class:
    """Добавляет конструктор к классу на основе аннотаций.
    Использует датаклассы с фиксированными параметрами:
        - kw_only = True
        - eq = False
        - repr = False
    """

    return dataclass(
        cls,
        kw_only=True,
        eq=False,
        repr=False,
    )


T = TypeVar('T')
Factory = Callable[[], T]

def factory(fn: Factory) -> field:
    return field(default_factory=fn)


no_init = field(init=False, default=None)
