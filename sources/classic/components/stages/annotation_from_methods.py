from copy import deepcopy
import inspect
from typing import Tuple, Any

import attr

from ..builder import AnyClass, Params, BuildStage


@attr.dataclass
class ExtendAnnotationFromMethods(BuildStage):
    dont_rewrite: bool = True

    def _get_extended_annotation(self, cls: AnyClass) -> Params:
        annotations = deepcopy(getattr(cls, '__annotations__', {}))

        members = inspect.getmembers(cls)
        for name, member in members:
            if callable(member):
                additional_properties = getattr(member, '__self_attrs__', None)
                if not additional_properties:
                    continue

                for prop_name, prop_type in additional_properties.items():
                    self._merge(annotations, prop_name, prop_type)

        return annotations

    def _merge(self, annotations, name, value):
        if name in annotations and self.dont_rewrite:
            return

        annotations[name] = value

    def build(self, cls: AnyClass, **params: Any) -> Tuple[AnyClass, Params]:
        cls.__annotations__ = self._get_extended_annotation(cls)
        return cls, params
