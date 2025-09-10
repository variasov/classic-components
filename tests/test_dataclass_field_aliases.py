from dataclasses import dataclass

from classic.components import default, factory, no_init


@dataclass
class SomeObj:
    prop_1: str = default('Hello')
    prop_2: list[str] = factory(list)
    prop_3: str = no_init('no init')


class test_aliases():
    obj = SomeObj()

    assert obj.prop_1 == 'Hello'
    assert obj.prop_2 == []
    assert obj.prop_3 == 'no init'
