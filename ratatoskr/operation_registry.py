from protectron import protectron
from schema import ValidOperationRegistryEventSchema
from operation_wrappers.base_wrappers import OperationWrapper, LocalOperation


class InvalidOperationWrapperError(Exception):
        pass


class OperationRegistry:

    registry = {}

    @classmethod
    def register_operation(cls, operation_wrapper):
        if not issubclass(operation_wrapper.__class__, OperationWrapper):
            raise InvalidOperationWrapperError("operation_wrapper must be a subclass of OperationWrapper")
        operation_name = operation_wrapper.get_wrapped_operation_name()
        OperationRegistry.registry[operation_name] = operation_wrapper

    @classmethod
    def deregister_operation(cls, operation_name):
        del OperationRegistry.registry[operation_name]

    @classmethod
    def list_operations(cls):
        return OperationRegistry.registry.keys()

    @classmethod
    def is_registered(cls, operation_name):
        return operation_name in OperationRegistry.registry

    @classmethod
    @protectron(input_schema=ValidOperationRegistryEventSchema())
    def call(cls, event):
        operation_name = event['operation']
        arguments = event['args']
        operation_wrapper = OperationRegistry.registry[operation_name]
        return operation_wrapper.call(**arguments)


def register_operation(operation_wrapper=LocalOperation()):

    def register_operation_decorator(func):

        operation_wrapper.load_wrapped_operation(func)
        OperationRegistry.register_operation(operation_wrapper)

        def func_wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        def peel_decorator():
            return func

        func_wrapper.peel_decorator = peel_decorator
        return func_wrapper

    return register_operation_decorator


def dispatch_operation(event):
    return OperationRegistry.call(event)
