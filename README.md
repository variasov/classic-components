# Classic Components

Предоставляет утилиты для удобного описания классов.

Главное, что предоставляет пакет - это декоратор component для обертывания 
классов. Класс, обернутый таким декоратором, называется далее компонентом,
и обладает рядом свойств:
- автоматически сгенерированный конструктор на базе аннотаций (dataclass).
- добавляет "дополнительные аннотации" к аннотациям класса (подробности далее)
- добавляет автоматическую регистрацию инстансов в указанных реестрах

Простой пример:

```python
from classic.components import component


@component
class SomeService:
    prop: int
    
    def action(self):
        print(self.prop)


service = SomeService(prop=1)
service.action()  # prints 1
```

Генерацию конструктора можно отключить:
```python
from classic.components import component


@component(init=False)
class SomeService:
    prop: int
    
    def action(self):
        print(self.prop)


service = SomeService(prop=1)  # TypeError: SomeService() takes no arguments
```

## Реестры

Также пакет предоставляет интерфейс для создания реестров и базовую реализацию
реестра со слабыми ссылками. Это нужно не столько для кода приложений, сколько
для других библиотек в платформе.

```python
from classic.components import component, Registry, WeakSetRegistry


@component(init=False)
class SomeService:
    registry: Registry
    
    def action(self):
        print(self.prop)


registry = WeakSetRegistry()
service = SomeService(registry=registry)

print(registry.storage)
# {<weakref at 0x109390fe0; to 'SomeService' at 0x10933ec50>}
```

## Алиасы для dataclasses.field

Также есть алиасы для часто используемых параметров field из dataclasses:
```python
from dataclasses import field
from classic.components import component, no_init, factory, default


@component
class SomeLogic:
    some_list: field(default_factory=list)
    analog: factory(list)  # то же самое
    
    some_str: str = field(default='Hello')
    analog_str: str = default('Hello')

    _some_field: int = field(default=0, init=False)
    _analog: int = no_init(0)  # то же самое
```