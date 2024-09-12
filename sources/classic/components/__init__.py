from .extra_annotations import (
    add_extra_annotation,
    extra_annotations,
    is_have_extra_annotations,
)
from .auto_init import auto_init
from .public_methods import wrap_public_methods
from .registries import Registry, WeakSetRegistry, auto_register
from .context_managers import wrap_context_manager
from .component import component, is_component
from .doublewrap import doublewrap
