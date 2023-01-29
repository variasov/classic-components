from typing import Type, Any, Dict, Callable


AnyClass = Type[Any]
Params = Dict[str, Any]
Method = Callable[[Type[Any], ...], Any]
