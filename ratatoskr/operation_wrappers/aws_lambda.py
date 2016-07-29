try:
    import boto3
except ImportError:
    raise ImportError('AWSLambdaOperation cannot be loaded'
                      'for "boto3" module is not found.')

import json

from base_wrappers import RemoteOperation


class AWSLambdaOperation(RemoteOperation):
    """
        OperationWrapper for calling other AWS Lambda functions
        where the operation is implemented.
    """

    def __init__(self, region, lambda_function):
        """
            @input `region` where the lambda function is present
            @input `lambda_function` name of the lambda function to be called
        """
        self.region = region
        self.lambda_function = lambda_function

    def call(self, *args, **kwargs):
        """
            Method that implements remote lambda call using `boto3`
            and parses the response.
        """
        cli = boto3.client('lambda', region_name=self.region)
        response = cli.invoke(
            FunctionName=self.lambda_function,
            Payload=json.dumps(kwargs)
        )
        return json.loads(response['Payload'].read())
