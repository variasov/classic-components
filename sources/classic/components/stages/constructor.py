from typing import Any, Tuple

import attr

from ..builder import AnyClass, Params, BuildStage


@attr.dataclass
class GenerateConstructor(BuildStage):
    init: bool = True
    kw_only: bool = True
    eq: bool = False
    repr: bool = False

    def build(self, cls: AnyClass, **params: Any) -> Tuple[AnyClass, Params]:
        if params.get('init', self.init):
            cls = attr.dataclass(
                cls,
                kw_only=params.get('kw_only', self.kw_only),
                eq=params.get('eq', self.eq),
                repr=params.get('repr', self.repr),
            )

        return cls, params
