import pytest

from ratatoskr import protectron, register_operation, dispatch_event
from voluptuous import Schema, Invalid


def test_register_operation_wraps_protectron_matching_schema():

    @register_operation
    @protectron(Schema({'a': int}))
    def mirror(a):
        return a

    event = {
        'operation': 'mirror',
        'args': {
            'a': 42
        }
    }

    assert dispatch_event(event) == 42


def test_register_operation_wraps_protectron_unmatching_schema():

    @register_operation
    @protectron(Schema({'a': int}))
    def mirror2(a):
        return a

    event = {
        'operation': 'mirror2',
        'args': {
            'a': '42'
        }
    }

    with pytest.raises(Invalid):
        assert dispatch_event(event) == 42



