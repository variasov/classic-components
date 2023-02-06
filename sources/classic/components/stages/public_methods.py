from dataclasses import dataclass
import inspect
from typing import Any, Tuple

from ..builder import AnyClass, BuildStage, Params


@dataclass
class WrapPublicMethods(BuildStage):

    def build(self, cls: AnyClass, **params: Any) -> Tuple[AnyClass, Params]:
        decorators = params.get('decorators')
        if not decorators:
            return cls, params

        public_methods = (
            (name, method)
            for name, method in inspect.getmembers(cls, callable)
            if not name.startswith('_')
        )

        for name, method in public_methods:
            for decorator in decorators:
                method = decorator(method)

            setattr(cls, name, method)

        return cls, params
