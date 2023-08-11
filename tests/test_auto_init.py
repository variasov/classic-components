import inspect

import pytest

from classic.components import component


@component
class SomeComponent:
    prop: int


@component
class SomeChild(SomeComponent):
    another_prop: str


@pytest.mark.parametrize(
    'cls,prop_name,prop_type', (
        (SomeComponent, 'prop', int),
        (SomeChild, 'prop', int),
        (SomeChild, 'another_prop', str),
    )
)
def test__annotations(cls, prop_name, prop_type):
    sig = inspect.signature(cls)

    assert prop_name in dict(sig.parameters)
    assert sig.parameters[prop_name].annotation == prop_type


def test__class__with__auto_init():
    instance = SomeComponent(prop=123)
    assert instance.prop == 123

    with pytest.raises(TypeError):
        SomeComponent()

    with pytest.raises(TypeError):
        SomeComponent(123)


def test__inheriting():
    instance = SomeChild(prop=123, another_prop='123')

    assert instance.prop == 123
    assert instance.another_prop == '123'
