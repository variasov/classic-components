from functools import update_wrapper
from typing import Any, Optional

from .extra_annotations import add_extra_annotation
from .types import Class, Method, Decorator, Function, Object


def _context_manager_wrapper(
    method: Method,
    attr: str,
    **ctx_mgr_kwargs: Any,
) -> Method:

    def wrapper(obj: Object, *args: Any, **kwargs: Any) -> Any:
        with getattr(obj, attr):
            return method(obj, *args, **kwargs)

    return wrapper


def _context_manager_call_wrapper(
    method: Method,
    attr: str,
    **ctx_mgr_kwargs: Any,
) -> Method:

    def wrapper(obj: Object, *args: Any, **kwargs: Any) -> Any:
        with getattr(obj, attr)(**ctx_mgr_kwargs):
            return method(obj, *args, **kwargs)

    return wrapper


def wrap_context_manager(
    default_prop: str,
    prop_type: Class,
    call_on_enter: bool = False,
) -> Decorator:
    """Функция для порождения декораторов из контекстных менеджеров
    с дополнительными аннотациями.

    Нужно для сокращения кода в случаях, когда необходимо обернуть в выражение
    with весь код в методе. Функция wrap_context_manager принимает на вход
    класс контекстного менеджера, которым будет декорироваться код, и дефолтное
    имя для свойства, из которого будет браться инстанс класса.

    Далее объяснение с примерами.

    Сначала пример менеджера контекста для использования в других примерах:
    >>> from contextlib import ContextDecorator
    ...
    ... class context(ContextDecorator):
    ...     def __enter__(self):
    ...         print('Starting')
    ...         return self
    ...
    ...     def __exit__(self, *exc):
    ...         print('Finishing')
    ...         return False

    Простой пример:
    >>> from classic.components import component
    ...
    ... @component
    ... class SomeClass:
    ...     some_dep: context
    ...
    ...    def some_method(self):
    ...        with self.some_dep:
    ...            # Предположим, что здесь много полезного кода
    ...            pass

    В этом примере весь полезный код будет сдвинут правее на один отступ из-за
    использования with. Можно попытаться использовать объект some_dep как
    декоратор, но мы не хотим привязывать классы к объектам, мы хотим
    использовать DI.

    Плохой пример:
    >>> class SomeClass:
    ...
    ... @context
    ... def some_method(self):
    ...     # Предположим, что здесь много полезного кода
    ...     pass

    В этом примере любой инстанс SomeClass будет связан с одним и тем же
    инстансом context, чего хотелось бы избежать. Тогда, мы могли бы пробросить
    context через конструктор, но при этом иметь такой декоратор, который бы
    делал обертывание через with:
    >>> # Простая версия декоратора
    ... def contextual(func):
    ...     def wrapper(*args, **kwargs):
    ...         self = args[0]
    ...         with self.some_dep:
    ...             return func(*args, **kwargs)
    ...
    ...     return wrapper
    ...
    ... @component
    ... class SomeCls:
    ...     some_dep: context
    ...
    ...     @contextual
    ...     def some_method(self):
    ...         # Предположим, что здесь много полезного кода
    ...         pass

    Функция wrap_context_manager позволяет не писать обертку-декоратор каждый
    раз, когда она нужна, позволяя сделать обертку:
    >>> contextual = wrap_context_manager(
    ...     'some_dep',  # Атрибут инстанса, который будет подставлен в with
    ...     context  # Класс, которому должен соответствовать атрибут
    ... )

    Также декораторы, порожденные wrap_context_manager, умеют добавлять к
    декорируемым методам название атрибута, которым они пользуются, и его тип.
    А декоратор component умеет автоматически добавлять такие аннотации от всех
    методов к общей аннотации класса, чтобы не приходилось каждый раз добавлять
    контекстный менеджер в класс вручную:
    >>> @component
    ... class SomeCls:
    ...
    ...     @contextual
    ...     def some_method(self):
    ...         # Предположим, что здесь много полезного кода
    ...         pass
    ...
    ... SomeCls.some_method.__extra_annotations__
    {'some_dep': context}
    >>> SomeCls.__annotations__
    {'some_dep': context}

    Полный пример:
    >>> # Это делается один раз, скорее всего, в библиотеках
    ... contextual = wrap_context_manager(
    ...     'some_dep',
    ...     context
    ... )
    ...
    ... @component
    ... class SomeCls:
    ...
    ...     @contextual
    ...     def some_method(self):
    ...         print('It works!')
    >>> instance = SomeCls(some_dep=context)
    >>> instance.some_method()
    Starting
    It works!
    Finishing
    """

    def decorator(
        original_method: Optional[Method] = None,
        attr: str = default_prop,
        **kwargs: Any,
    ):

        def decorate(function: Function) -> Function:
            if call_on_enter:
                wrapper = _context_manager_call_wrapper
            else:
                wrapper = _context_manager_wrapper

            wrapper = wrapper(function, attr, **kwargs)
            wrapper = update_wrapper(wrapper, function)
            wrapper = add_extra_annotation(wrapper, attr, prop_type)

            return wrapper

        if original_method:
            return decorate(original_method)

        return decorate

    return decorator
