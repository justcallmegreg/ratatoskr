import args_parser
import schema
import operation_registry
import operation_wrappers.base_wrappers as base_wrappers


def protectron(input_schema, output_schema=schema.EmptySchema()):

    def protectron_decorator(func):

        def func_wrapper(*args, **kwargs):
            args_dict = args_parser.args_to_dict(func, args)
            arguments = args_parser.merge_args_with_kwargs(args_dict, kwargs)
            arguments = input_schema(arguments)
            output = output_schema(func(*args, **kwargs))
            return output

        def peel_decorator():
            return func

        func_wrapper.peel_decorator = peel_decorator
        return func_wrapper

    return protectron_decorator


def register_operation(operation_wrapper=base_wrappers.LocalOperation()):

    def register_operation_decorator(func):

        operation_wrapper.load_wrapped_operation(func)
        operation_registry_cls = operation_registry.OperationRegistry
        operation_registry_cls.register_operation(operation_wrapper)

        def func_wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        def peel_decorator():
            return func

        func_wrapper.peel_decorator = peel_decorator
        return func_wrapper

    return register_operation_decorator


def dispatch_event(event):
    return operation_registry.OperationRegistry.call(event)
