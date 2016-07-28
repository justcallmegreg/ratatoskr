from protectron import protectron
from schema import ValidOperationRegistryEventSchema
from operation_wrappers.base_wrappers import OperationWrapper
from internal_logger import LOG


class InvalidOperationWrapperError(Exception):
    pass


class OperationAlreadyRegisteredError(Exception):
    pass


class OperationRegistry:

    registry = {}

    @classmethod
    def register_operation(cls, operation_wrapper):
        if not issubclass(operation_wrapper.__class__, OperationWrapper):

            LOG.error('operation_wrapper [%s] is not a sublass of OperationWrapper',
                      operation_wrapper.__class__)

            raise InvalidOperationWrapperError(
                'operation_wrapper must be a subclass of OperationWrapper'
            )

        operation_name = operation_wrapper.get_wrapped_operation_name()

        if operation_name in OperationRegistry.registry:
            LOG.error('operation [%s] is already registered in OperationRegistry',
                      operation_name)
            raise OperationAlreadyRegisteredError('%s' % operation_name)

        OperationRegistry.registry[operation_name] = operation_wrapper

        LOG.info('operation [%s] registered, operation_wrapper is [%s]',
                 operation_name, operation_wrapper.__class__)

    @classmethod
    def deregister_operation(cls, operation_name):
        del OperationRegistry.registry[operation_name]
        LOG.info('operation [%s] deregistered', operation_name)

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
        LOG.debug('event [%s] is dispatched to operation [%s]',
                  event, operation_name)
        LOG.info('operation [%s] is called',
                 operation_name)
        return operation_wrapper.call(**arguments)
