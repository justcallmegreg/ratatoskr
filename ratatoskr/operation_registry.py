from protectron import protectron
from schema import ValidOperationRegistryEventSchema
from operation_wrappers.base_wrappers import OperationWrapper
from internal_logger import LOG
from exceptions import (
    InvalidOperationWrapperError,
    OperationAlreadyRegisteredError,
    UnregisteredOperationError
)


class OperationRegistry:

    registry = {}

    @classmethod
    def register_operation(cls, operation_wrapper):
        """
            Method to store an operation in the registry.

            @raises: InvalidOperationWrapperError if `operation_wrapper`
            is not a sublass of OperationWrapper to ensure the neccesarry
            methods must be implemented
            @raises: OperationAlreadyRegisteredError if operation has been
            already registered
        """

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
        """
            Method to deregister an operation from the registry.

            After deregistering, the operation can't be called anymore.
        """
        if operation_name in OperationRegistry.registry:
            del OperationRegistry.registry[operation_name]
        LOG.info('operation [%s] deregistered', operation_name)

    @classmethod
    def list_operations(cls):
        """
            Method to list the current operations registered in the registry.

            Possible values for event['operation'].
        """
        return OperationRegistry.registry.keys()

    @classmethod
    def is_registered(cls, operation_name):
        """
            Returns if an operation is registered
        """
        return operation_name in OperationRegistry.registry

    @classmethod
    @protectron(input_schema=ValidOperationRegistryEventSchema())
    def call(cls, event):
        """
            Method to dispatch event according to `event['operation']`.

            Registry is searched for the operation by the registered name
            if found the connecting operation_wrapper's call method is executed
            that implements how to carry out the operation.
        """
        operation_name = event['operation']
        meta = event.get('meta', {})
        arguments = event.get('args', {})

        try:
            operation_wrapper = OperationRegistry.registry[operation_name]
        except KeyError:
            raise UnregisteredOperationError('operation [%s] is not registered' % operation_name)
        LOG.debug('event [%s] is dispatched to operation [%s]',
                  event, operation_name)
        LOG.info('operation [%s] is called',
                 operation_name)

        if meta.get('doc', False):
            return operation_wrapper.help()

        return operation_wrapper.call(**arguments)
