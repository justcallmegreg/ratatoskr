from internal_logger import LOG
from exceptions import SchemaValidationError


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
        required_keys = ['operation']
        if not isinstance(event, dict) or any([key not in payload for key in required_keys]):
            LOG.error('event schema validation failed, payload: %s', event)
            raise SchemaValidationError(
                '"event" is not a dict or "operation" is not specified'
            )
        return event
