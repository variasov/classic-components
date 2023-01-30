from .builder import BuildStage, Builder
from .utils import is_component, add_annotation, wrap_context_manager
from .registry import Registry

from . import stages


default_builder = Builder(
    stages.WrapPublicMethods(),
    stages.ExtendAnnotationFromMethods(),
    stages.GenerateConstructor(),
    stages.AddRegistrationOnInstantiation(),
)

component = default_builder.decorate
