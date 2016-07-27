from exceptions import Exception


class SchemaValidationError(Exception):
    pass


class EmptySchema:

    @classmethod
    def __call__(cls, event):
        return event


class ValidOperationRegistryEventSchema:

    @classmethod
    def __call__(cls, event):
        payload = event['event']
        has_operation = 'operation' in payload
        has_args = 'args' in payload
        if not isinstance(event, dict) or not has_operation or not has_args:
                raise SchemaValidationError(
                    '"event" is not a dict or "operation" is not specified'
                )
        return event
