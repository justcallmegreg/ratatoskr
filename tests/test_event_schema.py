import pytest

from ratatoskr import register_operation, dispatch_event
import ratatoskr


def test_operation_registry_empty_event():

    @register_operation(ratatoskr.base_wrappers.LocalOperation())
    def foo01():
        return 42

    event = {}

    with pytest.raises(ratatoskr.exceptions.SchemaValidationError):
        dispatch_event(event)


def test_operation_registry_missing_operation_field():

    @register_operation(ratatoskr.base_wrappers.LocalOperation())
    def bar01():
        return 42

    event = {
        'meta': {},
        'args': {}
    }

    with pytest.raises(ratatoskr.exceptions.SchemaValidationError):
        dispatch_event(event)


def test_operation_registry_missing_args_field():

    @register_operation(ratatoskr.base_wrappers.LocalOperation())
    def foo02():
        return 42

    event = {
        'operation': 'foo02',
        'meta': {}
    }

    assert dispatch_event(event) == 42


def test_operation_registry_missing_meta_field():

    @register_operation(ratatoskr.base_wrappers.LocalOperation())
    def foo03():
        return 42

    event = {
        'operation': 'foo03',
        'args': {}
    }

    assert dispatch_event(event) == 42


def test_operation_registry_meta_doc_field_true():

    @register_operation(ratatoskr.base_wrappers.LocalOperation())
    def foo04():
        """dummyDocumentation"""
        return 42

    event = {
        'operation': 'foo04',
        'meta': {
            'doc': True
        }
    }

    assert "dummyDocumentation" in dispatch_event(event)


def test_operation_registry_meta_doc_field_false():

    @register_operation(ratatoskr.base_wrappers.LocalOperation())
    def foo05():
        """dummyDocumentation"""
        return 42

    event = {
        'operation': 'foo05',
        'meta': {
            'doc': False
        }
    }

    assert dispatch_event(event) == 42
