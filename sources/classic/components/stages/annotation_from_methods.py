from dataclasses import dataclass
import inspect
from typing import Tuple, Any, Dict, get_type_hints

from ..builder import AnyClass, BuildStage, Params
from .. import utils


@dataclass
class ExtendAnnotationFromMethods(BuildStage):
    dont_rewrite: bool = True

    def build(self, cls: AnyClass, **params: Any) -> Tuple[AnyClass, Params]:
        cls.__annotations__ = self._get_extended_annotation(cls)
        return cls, params

    def _get_extended_annotation(self, cls: AnyClass) -> Params:
        annotations = get_type_hints(cls)

        members = inspect.getmembers(cls, utils.is_method_with_self_annotations)
        for __, member in members:
            for prop_name, prop_type in member.__self_attrs__.items():
                self._merge(annotations, prop_name, prop_type)

        return annotations

    def _merge(
        self, annotations: Dict[str, Any],
        name: str, value: Any,
    ) -> None:
        if name in annotations and self.dont_rewrite:
            return

        annotations[name] = value
