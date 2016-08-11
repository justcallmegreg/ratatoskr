import pytest

from ratatoskr import protectron
from voluptuous import Schema, Invalid, Required


def test_protectron_empty_input_schema():

    with pytest.raises(TypeError):

        @protectron()
        def foo(a):
            return a


def test_protectron_simple_input_schema_match():

    @protectron(Schema({'a': int}))
    def foo(a):
        return a

    assert foo(42) == 42


def test_protectron_simple_input_schema_unmatch():

    @protectron(Schema({'a': int}))
    def foo(a):
        return a

    with pytest.raises(Invalid):
        foo('42')


def test_protectron_kwargs_input_schema_match():

    @protectron(Schema({'a': int, 'b': int}))
    def foo(a, b):
        return a

    assert foo(a=42, b=42) == 42


def test_protectron_kwargs_input_schema_unmatch():

    @protectron(Schema({'a': int, 'b': int}))
    def foo(a, b):
        return a

    with pytest.raises(Invalid):
        foo(a='42', b=42)


def test_protectron_kwargs_input_schema_with_default():

    @protectron(Schema({Required('a', default=42): int, 'b': int}))
    def foo(a, b):
        return a

    assert foo(b=42) == 42


def test_protectron_empty_output_schema():

    with pytest.raises(TypeError):

        @protectron()
        def foo(a):
            return a


def test_protectron_simple_output_schema_match():

    @protectron(Schema({'a': int}), Schema(int))
    def foo(a):
        return a

    assert foo(42) == 42


def test_protectron_simple_output_schema_unmatch():

    @protectron(Schema({'a': int}), Schema(int))
    def foo(a):
        return a

    with pytest.raises(Invalid):
        foo('42')


# TODO: refactor testcase to check against tuple of integers
def test_protectron_multiple_output_schema_match():

    @protectron(Schema({'a': int, 'b': int}), Schema(tuple))
    def foo(a, b):
        return a, b

    assert foo(a=42, b=42) == (42, 42)


# TODO: refactor testcase to check against tuple of integers
def test_protectron_multiple_output_schema_unmatch():

    @protectron(Schema({'a': int, 'b': int}), Schema(int))
    def foo(a, b):
        return a, b

    with pytest.raises(Invalid):
        foo(a='42', b=42)


def test_protectron_kwargs_output_schema_match():

    input_schema = Schema({'a': int, 'b': int})
    output_schema = Schema(tuple)

    @protectron(input_schema, output_schema)
    def foo(a, b):
        return a, b

    foo(42, 42) == (42, 42)
