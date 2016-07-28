class OperationWrapper:

    def __init__(self):
        pass

    def load_wrapped_operation(self, func):
        self.wrapped_operation = func

    def get_wrapped_operation_name(self):
        return self.wrapped_operation.func_name

    def call(self, *args, **kwargs):
        raise NotImplementedError


class LocalOperation(OperationWrapper):

    def call(self, *args, **kwargs):
        return self.wrapped_operation(*args, **kwargs)


class RemoteOperation(OperationWrapper):
    pass
