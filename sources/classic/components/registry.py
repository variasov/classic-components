from abc import ABC, abstractmethod

from typing import Any


class Registry(ABC):

    @abstractmethod
    def register(self, obj: Any) -> None: ...

    @abstractmethod
    def unregister(self, obj: Any) -> None: ...
