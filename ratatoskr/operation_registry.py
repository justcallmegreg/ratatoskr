from protectron import protectron
from schema import ValidOperationRegistryEventSchema
from operation_wrappers.base_wrappers import OperationWrapper


class InvalidOperationWrapperError(Exception):
        pass


class OperationRegistry:

    registry = {}

    @classmethod
    def register_operation(cls, operation_wrapper):
        if not issubclass(operation_wrapper.__class__, OperationWrapper):
            raise InvalidOperationWrapperError(
                'operation_wrapper must be a subclass of OperationWrapper'
            )
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



