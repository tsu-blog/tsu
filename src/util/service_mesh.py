import datetime
import json
import boto3
import time
import os
from botocore.vendored import requests

lambda_client = boto3.client('lambda')

def call(service_name):
    start = time.time()
    invoke_response = lambda_client.invoke(
        FunctionName= os.environ['TSU_PREFIX'] + service_name,
        InvocationType='RequestResponse',
    )
    response_string = invoke_response['Payload'].read()
    response = json.loads(response_string)

    print("Util.service_mesh::call log -", service_name, (time.time()-start))

    if response.get('statusCode') == 200:
        return json.loads(response['body'])
    else:
        return response
