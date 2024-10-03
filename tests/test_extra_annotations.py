from classic.components import component, add_extra_annotation


def with_dep(prop_name, prop_type):

    def wrapper(fn):
        return add_extra_annotation(fn, prop_name, prop_type)

    return wrapper


@component
class SomeClass:

    def manually_annotated_method(self):
        return self.some_dep

    manually_annotated_method.__extra_annotations__ = {
        'some_dep': 'SomeDependency',
    }

    @with_dep('another_dep', 'SomeDependency')
    def func_annotated_method(self):
        return self.another_dep


@component
class Inheritor(SomeClass):

    @with_dep('another_dep', str)
    def func_annotated_method(self):
        return super().func_annotated_method()


class SomeDependency:
    attr: 'int'


def test_class():
    instance = SomeClass(some_dep=1, another_dep=2)

    assert instance.manually_annotated_method() == 1
    assert instance.func_annotated_method() == 2


def test_inheritor():
    instance = Inheritor(some_dep=1, another_dep=2)

    assert instance.manually_annotated_method() == 1
    assert instance.func_annotated_method() == 2

    assert Inheritor.__annotations__ == {
        'some_dep': 'SomeDependency',
        'another_dep': str,
    }
