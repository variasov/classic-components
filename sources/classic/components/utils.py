import inspect
from functools import update_wrapper
from typing import Any, Callable

from .types import AnyClass


AnyFunc = Callable[[...], Any]


def is_component(obj: AnyClass) -> bool:
    return hasattr(obj, '__parameters__')


def is_have_self_annotations(method: AnyFunc) -> bool:
    return hasattr(method, '__self_attrs__')


def is_method_with_self_annotations(method: Any) -> bool:
    return inspect.isfunction(method) and is_have_self_annotations(method)


def add_self_annotation(method: AnyFunc, key: str, value: Any) -> AnyFunc:
    if not hasattr(method, '__self_attrs__'):
        method.__self_attrs__ = {}

    method.__self_attrs__[key] = value

    return method


def context_manager_wrapper(
    method,
    prop_name: str,
    **ctx_mgr_kwargs: Any,
):
    def wrapper(obj, *args: Any, **kwargs: Any) -> Any:
        with getattr(obj, prop_name):
            return method(obj, *args, **kwargs)

    return wrapper


def context_manager_call_wrapper(
    method,
    prop_name: str,
    **ctx_mgr_kwargs: Any,
):
    def wrapper(obj, *args: Any, **kwargs: Any) -> Any:
        with getattr(obj, prop_name)(**ctx_mgr_kwargs):
            return method(obj, *args, **kwargs)

    return wrapper


def wrap_context_manager(
    default_prop: str,
    prop_type: AnyClass,
    call_on_enter: bool = False,
):

    def decorator(
        original_method=None,
        prop_name: str = default_prop,
        **kwargs: Any,
    ):

        def decorate(function):
            if call_on_enter:
                wrapper = context_manager_call_wrapper
            else:
                wrapper = context_manager_wrapper

            wrapper = wrapper(function, prop_name, **kwargs)
            wrapper = update_wrapper(wrapper, function)
            wrapper = add_self_annotation(wrapper, prop_name, prop_type)

            return wrapper

        if original_method:
            return decorate(original_method)

        return decorate

    return decorator
