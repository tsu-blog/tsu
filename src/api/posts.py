import datetime
import json
import boto3
from botocore.vendored import requests

lambda_client = boto3.client('lambda')

def handler(event, context):
    invoke_response = lambda_client.invoke(
        FunctionName="tsu-core-post-listing",
        InvocationType='RequestResponse',
    )
    response_string = invoke_response['Payload'].read()
    response = json.loads(response_string)
    print(response)

    body = {
        "posts": response
    }

    return {
        "statusCode": 200,
        "body": json.dumps(body)
    }
