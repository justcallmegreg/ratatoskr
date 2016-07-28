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
