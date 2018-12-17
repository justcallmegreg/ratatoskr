import utils
import operation_registry
import operation_wrappers.base_wrappers as base_wrappers
import types
import exceptions

from protectron import protectron


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


def deregister_operation(operation_name):

    operation_registry_cls = operation_registry.OperationRegistry
    operation_registry_cls.deregister_operation(operation_name)


def dispatch_event(event):
    return operation_registry.OperationRegistry.call(event)
