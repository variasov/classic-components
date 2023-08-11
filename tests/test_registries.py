from typing import Any

from classic.components import component, Registry, WeakSetRegistry, auto_register


class SimpleClass:
    pass


class SimpleRegistry(Registry):

    def __init__(self):
        self.storage = []

    def register(self, obj: Any) -> None:
        self.storage.append(obj)

    def unregister(self, obj: Any) -> None:
        self.storage.remove(obj)


@component
class SomeClass:
    registry: SimpleRegistry


@component
class SomeClassWithPostInit:
    registry: SimpleRegistry

    def __post_init__(self):
        self.prop = 'some_prop'


def test_auto_register():
    registry = SimpleRegistry()
    instance = SomeClass(registry=registry)

    assert instance in registry.storage


def test_auto_register_with_post_init():
    registry = SimpleRegistry()
    instance = SomeClassWithPostInit(registry=registry)

    assert instance in registry.storage
    assert instance.prop == 'some_prop'


def test__weakref_registry__with__manually__unregister():
    registry = WeakSetRegistry()
    instance = SimpleClass()

    registry.register(instance)
    assert instance in registry.storage

    registry.unregister(instance)
    assert len(registry.storage) == 0


def test__weakref_registry__with__del():
    registry = WeakSetRegistry()
    instance = SimpleClass()

    registry.register(instance)
    assert instance in registry.storage

    del instance
    assert len(registry.storage) == 0
