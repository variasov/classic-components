from typing import Optional

from .extra_annotations import extra_annotations
from .auto_init import auto_init
from .public_methods import wrap_public_methods, Decorators
from .registries import auto_register
from .types import Class, Decorator


def component(
    original_cls: Optional[Class] = None,
    *,
    init: bool = True,
    public_methods_wrappers: Decorators = None,
) -> Class | Decorator:
    """
    Декоратор, добавляющий к классу функциональность:
    - автоматически сгенерированный конструктор из аннотаций (по дефолту)
    - добавляет дополнительные аннотации из методов к аннотациям класса
    - оборачивает публичные методы в декораторы, указанные
      в public_methods_wrappers
    - добавляет функционал регистрации инстанса в известные ему реестры
      при инстанцировании класса
    """

    def decorate(cls: Class) -> Class:
        cls = extra_annotations(cls)

        if public_methods_wrappers:
            cls = wrap_public_methods(cls, public_methods_wrappers)

        cls = auto_register(cls)

        if init:
            cls = auto_init(cls)

        cls.__is_component__ = True

        return cls

    if original_cls:
        return decorate(original_cls)

    return decorate


def is_component(obj: Class) -> bool:
    """Предикат, определяющий, является ли объект компонентом"""

    return getattr(obj, '__is_component__', False)
