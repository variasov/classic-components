from typing import Any, Callable, TypeVar, Type, TypeAlias, Iterable


Function: TypeAlias = TypeVar('Function', bound=Callable[[...], Any])

Object: TypeAlias = TypeVar('Object', bound=object)
Class: TypeAlias = TypeVar('Class', bound=Type[object])
Method: TypeAlias = TypeVar('Method', bound=Callable[[object, ...], Any])

Decorable: TypeAlias = Function | Class
Decorator: TypeAlias = Callable[[Decorable, ...], Decorable]
Decorators: TypeAlias = Iterable[Decorator]
