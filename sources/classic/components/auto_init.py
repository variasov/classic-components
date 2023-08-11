from dataclasses import dataclass

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
