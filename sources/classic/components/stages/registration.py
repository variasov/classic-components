from functools import wraps
from typing import Any, Tuple, TypeVar, get_type_hints, Iterable

import attr

from ..builder import AnyClass, Params, BuildStage
from ..registry import Registry


T = TypeVar('T')


@attr.dataclass
class AddRegistrationOnInstantiation(BuildStage):
    registries: Tuple[str] = ()

    def build(self, cls: AnyClass, **params: Any) -> Tuple[AnyClass, Params]:
        registries = params.get('registries', self.registries)
        registries = registries or self._get_registries(cls)

        self._patch_init(cls, registries)
        self._patch_del(cls, registries)

        return cls, params

    @staticmethod
    def _get_registries(cls: T) -> Iterable[str]:
        annotations = get_type_hints(cls)
        registries = []
        for name, cls in annotations.items():
            try:
                if issubclass(cls, Registry):
                    registries.append(name)
            except TypeError:
                continue

        return registries

    @staticmethod
    def _patch_init(cls: T, registries: Iterable[str]) -> T:
        original_init = getattr(cls, '__init__', None)

        @wraps(original_init)
        def __init__(self, *args, **kwargs):
            original_init(self, *args, **kwargs)

            for registry_name in registries:
                registry = getattr(self, registry_name)
                registry.register(self)

        cls.__init__ = __init__

        return cls

    @staticmethod
    def _patch_del(cls: T, registries: Iterable[str]) -> T:
        original_del = getattr(cls, '__del__', None)

        @wraps(original_del)
        def __del__(self):
            for registry_name in registries:
                registry = getattr(self, registry_name)
                registry.unregister(self)

            if original_del:
                original_del()

        cls.__del__ = __del__

        return cls
