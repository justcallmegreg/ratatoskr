try:
    import boto3
except ImportError:
        raise ImportError('AWSLambdaOperation cannot be loaded'
                          'for "boto3" module is not found.')

import json

from base_wrappers import RemoteOperation


class AWSLambdaOperation(RemoteOperation):

    def __init__(self, region, lambda_function):
        self.region = region
        self.lambda_function = lambda_function

    def call(self, *args, **kwargs):
        cli = boto3.client('lambda', region_name=self.region)
        response = cli.invoke(
            FunctionName=self.lambda_function,
            Payload=json.dumps(kwargs)
        )
        return json.loads(response['Payload'].read())
