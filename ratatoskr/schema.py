from internal_logger import LOG


class SchemaValidationError(Exception):
    """
        Raised on unmatching schema.
    """
    pass


class EmptySchema:
    """
        Matches any payload.
    """

    @classmethod
    def __call__(cls, event):
        return event


class ValidOperationRegistryEventSchema:
    """
        Matches if the `event` has all the required keys.
    """

    @classmethod
    def __call__(cls, event):
        payload = event['event']
        has_operation = 'operation' in payload
        has_args = 'args' in payload
        if not isinstance(event, dict) or not has_operation or not has_args:
            LOG.error('event schema validation failed, payload: %s', event)
            raise SchemaValidationError(
                '"event" is not a dict or "operation" is not specified'
            )
        return event
