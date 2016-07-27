import sys


def args_to_dict(func, args):
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


def merge_args_with_kwargs(args_dict, kwargs_dict):
    ret = args_dict.copy()
    ret.update(kwargs_dict)
    return ret
