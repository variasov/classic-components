import inspect

import pytest

from classic.components import component, is_component


class JustAClass:
    pass


@component
class SomeComponent:
    prop: int


@component
class SomeChild(SomeComponent):
    another_prop: str


@component(init=False)
class ComponentWithCustomInit:

    def __init__(self, prop: int):
        self.prop = prop

    def some_method(self):
        pass


@pytest.mark.parametrize(
    'cls,prop_name,prop_type', (
        (SomeComponent, 'prop', int),
        (SomeChild, 'prop', int),
        (SomeChild, 'another_prop', str),
        (ComponentWithCustomInit, 'prop', int),
    )
)
def test_annotations(cls, prop_name, prop_type):
    sig = inspect.signature(cls)

    assert prop_name in sig.parameters
    assert sig.parameters[prop_name].annotation == prop_type


def test_class_component():
    instance = SomeComponent(prop=123)
    assert instance.prop == 123

    with pytest.raises(TypeError):
        SomeComponent()

    with pytest.raises(TypeError):
        SomeComponent(123)


def test_inheriting():
    instance = SomeChild(prop=123, another_prop='123')

    assert instance.prop == 123
    assert instance.another_prop == '123'


def test_without_auto_constructor():
    assert hasattr(ComponentWithCustomInit, 'some_method')
    instance = ComponentWithCustomInit(prop=123)

    assert isinstance(instance, ComponentWithCustomInit)
    assert instance.prop == 123
    assert hasattr(instance, 'some_method')


def test_is_component():
    assert is_component(SomeComponent)
    assert not is_component(JustAClass)
