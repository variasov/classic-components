from .builder import BuildStage, Builder
from .constructor import GenerateConstructor
from .annotation_from_methods import ExtendAnnotationFromMethods, add_annotation
from .public_methods import WrapPublicMethods
from .context_managers import wrap_context_manager
from .utils import is_component


default_builder = Builder(
    WrapPublicMethods(),
    ExtendAnnotationFromMethods(),
    GenerateConstructor(),
)

component = default_builder.decorate
