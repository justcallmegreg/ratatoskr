class OperationWrapper:
    """
        Base class that wraps functions and implements how to execute them.
    """

    def __init__(self):
        pass

    def load_wrapped_operation(self, func):
        """
            Loads the wrapped operation into the OperationWrapper
            for later use.
        """
        self.wrapped_operation = func

    def get_wrapped_operation_name(self):
        """
            Returns the name (id) of the operation that was loaded
            into OperatioWrapper.
        """
        return self.wrapped_operation.func_name

    def help(self):
        """
            Method that returns documentation for the wrapped given function.
        """
        return self.wrapped_operation.__doc__

    def call(self, *args, **kwargs):
        """
            Method that implements the way of calling the wrapped function.

            @raises NotImplementedError if this function is notimplemented in the subclasses
        """
        raise NotImplementedError


class LocalOperation(OperationWrapper):
    """
        Class to represent operations that must be executed on the host.
    """
    def __init__(self, custom_name=str()):
        self.custom_name = custom_name

    def get_wrapped_operation_name(self):
        """
            Returns the name (id) of the operation that was loaded
            into OperatioWrapper.
        """
        return self.custom_name if self.custom_name != "" else self.wrapped_operation.func_name

    def call(self, *args, **kwargs):
        return self.wrapped_operation(*args, **kwargs)


class RemoteOperation(OperationWrapper):
    """
        Base class to represent operations that must be executed on remote hosts.
    """
    pass
