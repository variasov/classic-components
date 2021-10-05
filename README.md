# Classic Components

This package provides decorator for creating components with 
explicitly defined dependencies for Dependency Injection.
Decorator marks class as component and, optionally, generates constructor from 
type annotations.

Part of project "Classic".

Usage:

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
