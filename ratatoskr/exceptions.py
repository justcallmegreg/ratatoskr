class InvalidOperationWrapperError(Exception):
    """
        Raised when the custom user-provided operation wrapper does
        not meet some requirements.
    """
    pass


class OperationAlreadyRegisteredError(Exception):
    """
        Raised upon attempt to register an operation with a name that
        is already present in the registry
    """
    pass


class UnregisteredOperationError(Exception):
    """
        Raised on dispatching event with unregistered oparation field
    """
    pass


class SchemaValidationError(Exception):
    """
        Raised on unmatching schema.
    """
    pass


class UnauthorizedAccessError(Exception):
    """
        Raised on dispatching event to a a resource that cannot be
        used with the claimed identity.
    """
    pass


