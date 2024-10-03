from abc import ABC, abstractmethod
from typing import Any, ClassVar, Iterable
from weakref import WeakSet

from .types import Class, Object


class Registry(ABC):
    """Интерфейс для реестра объектов"""

    @abstractmethod
    def register(self, obj: Any) -> None: ...

    @abstractmethod
    def unregister(self, obj: Any) -> None: ...


class WeakSetRegistry(Registry):
    """Реестр объектов, хранящий слабые ссылки на объекты.

    >>> registry = WeakSetRegistry()
    >>> class SomeClass:
    ...     pass
    ...
    >>> instance = SomeClass()
    >>> registry.register(instance)
    >>> registry.storage
    {<weakref at 0x109390fe0; to 'SomeCls' at 0x10933ec50>}
    """

    storage: WeakSet[Any]

    __is_component__: ClassVar[bool] = True

    def __init__(self):
        self.storage = WeakSet()

    def register(self, obj: Any) -> None:
        self.storage.add(obj)

    def unregister(self, obj: Any) -> None:
        self.storage.remove(obj)


def auto_register(cls: Class) -> Class:
    """Декоратор, добавляющий регистрацию инстанса класса  при инстанцировании
    во всех реестрах, известных это классу.

    >>> @auto_register
    ... class SomeClass:
    ...     some_reg: Registry
    ...
    >>> registry = WeakSetRegistry()
    >>> instance = SomeClass(some_reg=registry)
    >>> registry.storage
    {<weakref at 0x109390fe0; to 'SomeCls' at 0x10933ec50>}
    """

    registries = _inspect_registries(cls)
    if not registries:
        return cls

    return _patch_post_init(cls, registries)


def register_instance(obj: Object, registries: Iterable[str]):
    """Регистрирует объект в указанных реестрах.
    Объект должен содержать ссылку на реестры в атрибутах.
    """

    for registry_name in registries:
        registry = getattr(obj, registry_name)
        registry.register(obj)


def unregister_instance(obj: Object, registries: Iterable[str]):
    """Дерегистрирует объект в указанных реестрах.
    Объект должен содержать ссылку на реестры в атрибутах.
    """

    for registry_name in registries:
        registry = getattr(obj, registry_name)
        registry.unregister(obj)


def _inspect_registries(cls: Class) -> Iterable[str]:
    registries = []
    for name, cls in cls.__annotations__.items():
        try:
            if issubclass(cls, Registry):
                registries.append(name)
        except TypeError:
            continue

    return registries


def _patch_post_init(cls: Class, registries: Iterable[str]) -> Class:
    original_post_init = getattr(cls, '__post_init__', None)

    if original_post_init:

        def post_init(self):
            original_post_init(self)
            register_instance(self, registries)

    else:

        def post_init(self):
            register_instance(self, registries)

    cls.__post_init__ = post_init

    return cls
