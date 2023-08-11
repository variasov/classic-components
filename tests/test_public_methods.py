from classic.components import component


def some_decorator(func):
    func.__decorated__ = True
    return func


@component(public_methods_wrappers=[some_decorator])
class SomeClass:

    def public_method(self):
        return 'public'

    def _protected_method(self):
        return 'protected'


def test__public__methods__wrapping():
    assert hasattr(SomeClass.public_method, '__decorated__')
    assert not hasattr(SomeClass._protected_method, '__decorated__')
