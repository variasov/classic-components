import dataclasses
from typing import Callable, Any


Factory = Callable[[], Any]


def factory(fn: Factory, **kwargs: Any) -> dataclasses.field:
    """
    Алиас для dataclasses.field с заполненным ключом default_factory.
    Сахар для сокращения шаблонного кода.
    >>> from dataclasses import dataclass, field
    ... @dataclass
    ... class Example:
    ...     # Очень длинная запись
    ...     some_prop: list[int] = field(default_factory=list)
    ...     # Аналог с factory:
    ...     another_prop: list[int] = factory(list)
    """
    return dataclasses.field(default_factory=fn, **kwargs)


def default(value: Any, **kwargs: Any) -> dataclasses.field:
    """
    Алиас для dataclasses.field с заполненным ключом default.
    Сахар для сокращения шаблонного кода.
    В основном, нужен в случаях, когда аргументов у field больше одного.
    >>> from dataclasses import dataclass, field
    ... @dataclass
    ... class Example:
    ...     # Обычная запись без дополнительных аргументов коротка,
    ...     # в ней нечего улучшать
    ...     some_prop: int = 0
    ...     # Но если появляется хотя бы один параметр,
    ...     # запись становится достаточно длинной:
    ...     other_prop: int = field(default=0, init=False)
    ...     # Аналог с default:
    ...     another_prop: int = default(0, init=False)
    """
    return dataclasses.field(default=value, **kwargs)


def no_init(
    default: Any = dataclasses.MISSING,
    factory: Callable[[], Any] = dataclasses.MISSING,
    **kwargs: Any,
) -> dataclasses.field:
    """
    Алиас для dataclasses.field с заполненным ключом init.
    Сахар для сокращения шаблонного кода.
    >>> from dataclasses import dataclass, field
    ... @dataclass
    ... class Example:
    ...     # Очень длинная запись:
    ...     prop_1: int = field(default=0, init=False)
    ...     # Аналог с no_init:
    ...     prop_2: list[int] = no_init(default=0)
    ...     # Или еще короче:
    ...     prop_3: list[int] = no_init(0)
    ...     # Очень длинная запись с фабрикой:
    ...     prop_4: list[int] = field(default_factory=list, init=False)
    ...     # Аналог с no_init:
    ...     prop_5: list[int] = no_init(factory=list)
    """
    return dataclasses.field(
        default=default,
        default_factory=factory,
        init=False,
        **kwargs,
    )
