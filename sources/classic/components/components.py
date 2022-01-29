from typing import Type, Dict, Any
import inspect

import attr


registry = []


FUNCTION = 'function'
CLASS = 'class'


def _extend_annotation_from_methods(cls):
    members = inspect.getmembers(cls)
    for name, member in members:
        if callable(member):
            additional_properties = getattr(member, '__cls_properties__', {})
            if not additional_properties:
                continue

            if not hasattr(cls, '__annotations__'):
                setattr(cls, '__annotations__', {})

            for prop_name, prop_type in additional_properties.items():
                cls.__annotations__[prop_name] = prop_type
    return cls


@attr.dataclass
class ComponentParameters:
    init: bool
    params: Dict[str, Any]
    type: str = None


def component(original_obj: Type = None, init: bool = True, **kwargs: Any):
    """
    Mark class as component, and, optionally, creates constructor for
    dependency injection. Dependencies must be described
    with type annotations.
    """

    # Attrs is used instead of dataclasses, because with attrs we can
    # mark all args as keyword. This allows inheriting of components.
    # In case of using of dataclasses we will see next situation:
    #
    # >>> from dataclasses import dataclass
    # ...
    # >>> @dataclass
    # ... class Example:
    # ...     some: str = 'default'
    # ...
    # >>>
    # >>> @dataclass
    # ... class Inheritor(Example):
    # ...     another: str
    # ...
    # TypeError: non-default argument 'another' follows default argument

    def _decorate(obj):
        setattr(obj, '__component__', ComponentParameters(init, kwargs))

        if inspect.isfunction(obj):
            obj.__component__.type = FUNCTION

        elif inspect.isclass(obj):
            obj.__component__.type = CLASS

            obj = _extend_annotation_from_methods(obj)
            if init:
                obj = attr.dataclass(obj, kw_only=True, eq=False, repr=False)
        else:
            raise ValueError(f'Component {obj} must be class or function')

        registry.append(obj)

        return obj

    if original_obj:
        return _decorate(original_obj)

    return _decorate


def is_component(cls: Type) -> bool:
    return hasattr(cls, '__component__')


def is_class_component(obj) -> bool:
    return is_component(obj) and obj.__component__.type == CLASS


def is_function_component(obj) -> bool:
    return is_component(obj) and obj.__component__.type == FUNCTION
