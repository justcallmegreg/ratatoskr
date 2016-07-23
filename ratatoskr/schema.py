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
        if not isinstance(event, dict) or 'operation' not in event['event']:
                raise SchemaValidationError(
                    '"event" is not a dict or "operation" is not specified'
                )
        return event
