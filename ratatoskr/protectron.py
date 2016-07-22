import sys

from schema import EmptySchema


def _args_to_dict(func, args):
    if sys.version_info >= (3, 0):
        arg_count = func.__code__.co_argcount
        arg_names = func.__code__.co_varnames[:arg_count]
    else:
        arg_count = func.func_code.co_argcount
        arg_names = func.func_code.co_varnames[:arg_count]

    arg_value_list = list(args)
    arguments = dict((arg_name, arg_value_list[i])
                     for i, arg_name in enumerate(arg_names)
                     if i < len(arg_value_list))
    return arguments


def _merge_args_with_kwargs(args_dict, kwargs_dict):
    ret = args_dict.copy()
    ret.update(kwargs_dict)
    return ret


def protectron(input_schema, output_schema=EmptySchema()):

    def protectron_decorator(func):

        def func_wrapper(*args, **kwargs):
            args_dict = _args_to_dict(func, args)
            arguments = _merge_args_with_kwargs(args_dict, kwargs)
            input_schema(arguments)
            return output_schema(func(*args, **kwargs))

        def peel_decorator():
            return func

        func_wrapper.peel_decorator = peel_decorator
        return func_wrapper

    return protectron_decorator
