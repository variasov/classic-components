from .types import AnyClass


def is_component(obj: AnyClass) -> bool:
    return hasattr(obj, '__parameters__')
