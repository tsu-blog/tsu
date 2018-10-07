import datetime
import json
import boto3
from botocore.vendored import requests

lambda_client = boto3.client('lambda')

#somewhere else...
# posts = util.service.call('post-listing')

def call(service_name):
    invoke_response = lambda_client.invoke(
        FunctionName="tsu-" + service_name,
        InvocationType='RequestResponse',
    )
    response_string = invoke_response['Payload'].read()
    response = json.loads(response_string)
    return response
