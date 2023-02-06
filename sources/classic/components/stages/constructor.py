from dataclasses import dataclass
import inspect
from typing import Any, Tuple

from ..builder import AnyClass, BuildStage, Params


@dataclass
class GenerateConstructor(BuildStage):
    init: bool = True
    kw_only: bool = True
    eq: bool = False
    repr: bool = False

    def build(self, cls: AnyClass, **params: Any) -> Tuple[AnyClass, Params]:
        if not self._is_have_init(cls) and params.get('init', self.init):
            cls = dataclass(
                cls,
                kw_only=params.get('kw_only', self.kw_only),
                eq=params.get('eq', self.eq),
                repr=params.get('repr', self.repr),
            )

        return cls, params

    @staticmethod
    def _is_have_init(cls: AnyClass) -> bool:
        return inspect.isfunction(cls.__init__)
