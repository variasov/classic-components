from contextlib import AbstractContextManager
from unittest.mock import MagicMock

from pytest import fixture
from classic.components import (
    component, make_method_decorator, make_context_manager_wrapper
)

contextual = make_method_decorator(
    make_context_manager_wrapper,
    'context_manager',
    AbstractContextManager
)


@component
class SomeCls:
    unused_dep: str

    @contextual
    def method1(self):
        return 1

    @contextual(prop_name='context_manager_2')
    def method2(self):
        return 2


@fixture
def ctx_manager_1():
    return MagicMock(AbstractContextManager)


@fixture
def ctx_manager_2():
    return MagicMock(AbstractContextManager)


@fixture
def obj(ctx_manager_1, ctx_manager_2):
    return SomeCls(unused_dep='unused',
                   context_manager=ctx_manager_1,
                   context_manager_2=ctx_manager_2)


def test_default_prop_name(obj, ctx_manager_1, ctx_manager_2):

    result1 = obj.method1()

    assert result1 == 1

    ctx_manager_1.__enter__.assert_called()
    ctx_manager_1.__exit__.assert_called()
    ctx_manager_2.__enter__.assert_not_called()
    ctx_manager_2.__exit__.assert_not_called()


def test_custom_prop_name(obj, ctx_manager_1, ctx_manager_2):
    result2 = obj.method2()

    assert result2 == 2

    ctx_manager_1.__enter__.assert_not_called()
    ctx_manager_1.__exit__.assert_not_called()
    ctx_manager_2.__enter__.assert_called()
    ctx_manager_2.__exit__.assert_called()
