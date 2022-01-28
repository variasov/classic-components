from functools import update_wrapper


def make_context_manager_wrapper(function, prop_name, **decorator_kwargs):
    def wrapper(obj, *args, **kwargs):
        with getattr(obj, prop_name):
            return function(obj, *args, **kwargs)

    return wrapper


def make_method_decorator(make_wrapper, default_prop, prop_type):

    def decorator(original_method=None, prop_name=default_prop, **kwargs):

        def decorate(function):
            wrapper = make_wrapper(function, prop_name, **kwargs)
            wrapper = update_wrapper(wrapper, function)

            if '__cls_properties__' not in wrapper.__dict__:
                setattr(wrapper, '__cls_properties__', {})

            wrapper.__cls_properties__[prop_name] = prop_type

            return wrapper

        if original_method:
            return decorate(original_method)

        return decorate

    return decorator
