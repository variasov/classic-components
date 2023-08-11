from contextlib import AbstractContextManager
from unittest.mock import MagicMock

from pytest import fixture
from classic.components import component, wrap_context_manager


contextual = wrap_context_manager(
    'context_manager',
    AbstractContextManager
)


@component
class SomeCls:
    unused_dep: str

    @contextual
    def some_method(self):
        return 'some'

    @contextual(attr='context_manager_2')
    def another_method(self):
        return 'another'


@fixture
def ctx_manager_1():
    return MagicMock(spec=AbstractContextManager)


@fixture
def ctx_manager_2():
    return MagicMock(spec=AbstractContextManager)


@fixture
def obj(ctx_manager_1, ctx_manager_2):
    return SomeCls(unused_dep='unused',
                   context_manager=ctx_manager_1,
                   context_manager_2=ctx_manager_2)


def test__default__prop_name(obj: SomeCls, ctx_manager_1, ctx_manager_2):
    result1 = obj.some_method()

    assert result1 == 'some'

    ctx_manager_1.__enter__.assert_called()
    ctx_manager_1.__exit__.assert_called()
    ctx_manager_2.__enter__.assert_not_called()
    ctx_manager_2.__exit__.assert_not_called()


def test__custom__prop_name(obj: SomeCls, ctx_manager_1, ctx_manager_2):
    result2 = obj.another_method()

    assert result2 == 'another'

    ctx_manager_1.__enter__.assert_not_called()
    ctx_manager_1.__exit__.assert_not_called()
    ctx_manager_2.__enter__.assert_called()
    ctx_manager_2.__exit__.assert_called()
