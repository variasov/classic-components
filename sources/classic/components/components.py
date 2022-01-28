from typing import Type, Any
import inspect

import attr


registry = []


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


def component(original_cls: Type = None, init: bool = True, **kwargs: Any):
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

    def _decorate(cls):
        setattr(cls, '__component__', {
            'params': kwargs,
            'init': init,
        })

        cls = _extend_annotation_from_methods(cls)

        if init:
            cls = attr.dataclass(cls, kw_only=True, eq=False, repr=False)

        registry.append(cls)

        return cls

    if original_cls:
        return _decorate(original_cls)

    return _decorate


def is_component(cls: Type) -> bool:
    return hasattr(cls, '__component__')
