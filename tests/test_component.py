import pytest

from classic.components import (
    component, is_component, is_class_component, is_function_component,
)


@component
class SomeCls:
    prop: int


@component
class Child(SomeCls):
    another_prop: str


@component(init=False)
class ClsWithInit:

    def __init__(self, prop: int):
        self.prop = prop


@component
def some_func(arg):
    return arg


def test_class_component():
    instance = SomeCls(prop=123)
    assert instance.prop == 123

    with pytest.raises(TypeError):
        SomeCls()

    with pytest.raises(TypeError):
        SomeCls(123)


def test_inheriting():
    instance = Child(prop=123, another_prop='123')

    assert instance.prop == 123
    assert instance.another_prop == '123'


def test_without_auto_constructor():
    instance = ClsWithInit(prop=123)

    assert instance.prop == 123
    assert instance.__component__


def test_checks():
    assert is_component(SomeCls)

    assert is_class_component(SomeCls)
    assert not is_function_component(SomeCls)

    assert is_function_component(some_func)
    assert not is_class_component(some_func)


def test_func_component():
    result = some_func(1)

    assert result == 1
