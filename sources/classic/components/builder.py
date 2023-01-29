from functools import partial
from typing import Any, Tuple

from .types import AnyClass, Params


class BuildStage:

    def build(
        self, cls: AnyClass, **params: Any
    ) -> Tuple[AnyClass, Params]: ...


class Builder:
    stages: list[BuildStage]

    def __init__(self, *stages: BuildStage):
        self.stages = stages or []

    def build(self, cls: AnyClass, **params: Any) -> AnyClass:
        for stage in self.stages:
            cls, params = stage.build(cls, **params)

        cls.__parameters__ = params

        return cls

    def decorate(self, cls: AnyClass = None, **kwargs: Any):
        if cls:
            return self.build(cls, **kwargs)

        return partial(self.decorate, **kwargs)
