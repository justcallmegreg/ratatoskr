import utils
import schema
import operation_registry
import operation_wrappers.base_wrappers as base_wrappers
import types


def protectron(input_schema, output_schema=schema.EmptySchema()):

    def protectron_decorator(func):

        def func_wrapper(*args, **kwargs):
            args_dict = utils.args_to_dict(func, args)
            arguments = utils.merge_args_with_kwargs(args_dict, kwargs)
            arguments = input_schema(arguments)
            output = output_schema(func(*args, **kwargs))
            return output

        def peel_decorator():
            return func

        func_wrapper.peel_decorator = peel_decorator
        return func_wrapper

    return protectron_decorator


@utils.doublewrap
def register_operation(func, operation_wrapper=base_wrappers.LocalOperation):

    if isinstance(operation_wrapper, types.ClassType):
        operation_wrapper_instance = operation_wrapper()
    else:
        operation_wrapper_instance = operation_wrapper

    operation_wrapper_instance.load_wrapped_operation(func)
    operation_registry_cls = operation_registry.OperationRegistry
    operation_registry_cls.register_operation(operation_wrapper_instance)

    @utils.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def dispatch_event(event):
    return operation_registry.OperationRegistry.call(event)
