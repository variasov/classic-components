from typing import Type

import attr


def component(original_cls: Type = None, init: bool = True):
    """
    Mark class as component, and, optionally, creates constructor for
    dependency injection. Dependencies must be described with type annotations.
    """

    # We using attrs instead of dataclasses, because with attrs we can
    # mark all args as keyword. This allows inheriting of components.
    # In case of useing of dataclasses we will see next situation:
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
        setattr(cls, '__component__', True)

        if init:
            cls = attr.dataclass(cls, eq=False, kw_only=True)

        return cls

    if original_cls:
        return _decorate(original_cls)

    return _decorate
