import utils
import schema


def protectron(input_schema, output_schema=schema.EmptySchema()):

    def protectron_decorator(func):

        def func_wrapper(*args, **kwargs):
            args_dict = utils.args_to_dict(func, args)
            arguments = utils.merge_args_with_kwargs(args_dict, kwargs)
            arguments = input_schema(arguments)
            output = output_schema(func(*args, **kwargs))
            return output

        def peel_decorator():
            return func

        func_wrapper.peel_decorator = peel_decorator
        return func_wrapper

    return protectron_decorator
