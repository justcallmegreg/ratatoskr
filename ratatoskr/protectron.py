import utils
import schema

from internal_logger import LOG


def protectron(input_schema, output_schema=schema.EmptySchema()):
    """
        Decorator for validating inputs and outputs according to the given
        schema.

        Both input and output schema must be a callable object, that
        raises `SchemaValidationException` if the schema is not fitting
        the payload, returning the payload otherwise

        @input `input_schema` is tested against the arguments of the function
        @input `output_schema` is tested against the return value of the function

        @default `output_schema` is tested against EmptySchema by default that
        matches any payload

    """
    def protectron_decorator(func):

        @utils.wraps(func)
        def func_wrapper(*args, **kwargs):
            args_dict = utils.args_to_dict(func, args)
            arguments = utils.merge_args_with_kwargs(args_dict, kwargs)
            arguments = input_schema(arguments)

            LOG.debug('input schema [%s] is applied to arguments [%s]',
                      input_schema, arguments)

            output = output_schema(func(**arguments))

            LOG.debug('output schema [%s] is applied to return value[%s]',
                      output_schema, output)

            return output

        return func_wrapper

    return protectron_decorator
