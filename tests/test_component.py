import pytest

from classic.components import component


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


def test_component():
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
    assert instance.__component__ is True
