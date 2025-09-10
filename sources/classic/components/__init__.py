from .extra_annotations import (
    add_extra_annotation,
    extra_annotations,
    is_have_extra_annotations,
)
from .auto_init import auto_init
from .dataclass_field_aliases import factory, default, no_init
from .public_methods import wrap_public_methods
from .registries import Registry, WeakSetRegistry, auto_register
from .component import component, is_component
from .doublewrap import doublewrap
