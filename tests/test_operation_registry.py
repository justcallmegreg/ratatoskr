import pytest

from ratatoskr import register_operation, dispatch_event
import ratatoskr

def test_operation_dispatch():

    @register_operation()
    def foo():
        return 42

    @register_operation()
    def bar():
        return 24

    event = {
        'operation': 'foo',
        'args': {}
    }

    assert dispatch_event(event) == 42


def test_operation_dispatch_with_custom_operation_wrapper():

    @register_operation(ratatoskr.base_wrappers.LocalOperation())
    def foo2():
        return 42

    @register_operation(ratatoskr.base_wrappers.LocalOperation())
    def bar2():
        return 24

    event = {
        'operation': 'foo2',
        'args': {}
    }

    assert dispatch_event(event) == 42


def test_operation_dispatch_with_args():

    @register_operation()
    def foo3(value):
        return value

    event = {
        'operation': 'foo3',
        'args': {'value': 69}
    }

    assert dispatch_event(event) == 69


def test_decorator_without_parantheses():

    @register_operation
    def foo4(value):
        return value

    event = {
        'operation': 'foo4',
        'args': {'value': 69}
    }

    assert dispatch_event(event) == 69


def test_decorator_multiple_registartions():

    @register_operation
    def foo5(value):
        return value

    with pytest.raises(ratatoskr.operation_registry.OperationAlreadyRegisteredError):

        @register_operation
        def foo4(value):
            return value

    event = {
        'operation': 'foo4',
        'args': {'value': 69}
    }

    assert dispatch_event(event) == 69


def test_event_structure_missing_operation():

    @register_operation
    def foo6(value):
        return value

    event = {
    }

    with pytest.raises(ratatoskr.schema.SchemaValidationError):
        assert dispatch_event(event) == 69


def test_operation_wrapper_is_not_subclass():

    class DummyOperationWrapper:

        def load_wrapped_operation(self, func):
            self.wrapped_operation = func

        def get_wrapped_operation_name(self):
            return self.wrapped_operation.func_name

    with pytest.raises(ratatoskr.operation_registry.InvalidOperationWrapperError):

        @register_operation(operation_wrapper=DummyOperationWrapper())
        def foo7(value):
            return value

    event = {
        'operation': 'foo4',
        'args': {'value': 69}
    }

    assert dispatch_event(event) == 69


def test_operation_registry_list_operations():

    @register_operation
    def foo9(value):
        return value

    assert 'foo9' in ratatoskr.operation_registry.OperationRegistry.list_operations()


def test_operation_registry_deregister_operation():

    @register_operation
    def foo10(value):
        return value

    ratatoskr.operation_registry.OperationRegistry.deregister_operation('foo10')

    assert 'foo10' not in ratatoskr.operation_registry.OperationRegistry.list_operations()


def test_operation_registry_is_registered():

    @register_operation
    def foo11(value):
        return value

    assert ratatoskr.operation_registry.OperationRegistry.is_registered('foo11')


def test_operation_wrapper_call_is_not_implemented():

    class DummyOperationWrapper(ratatoskr.operation_wrappers.base_wrappers.OperationWrapper):

        def load_wrapped_operation(self, func):
            self.wrapped_operation = func

        def get_wrapped_operation_name(self):
            return self.wrapped_operation.func_name

    @register_operation(operation_wrapper=DummyOperationWrapper())
    def foo12(value):
        return value

    event = {
        'operation': 'foo12',
        'args': {'value': 69}
    }

    with pytest.raises(NotImplementedError):
        assert dispatch_event(event) == 69


def test_operation_registry_unregistered_operation():

    event = {
        'operation': 'dummy_unregistered_operation',
        'args': {}
    }

    with pytest.raises(ratatoskr.operation_registry.UnregisteredOperationError):
        dispatch_event(event)
