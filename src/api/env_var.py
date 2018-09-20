import os
import json

def handler(event, context):
    # TODO implement
    env_var_dict = {
        'time': os.environ['TZ'],
        'runtime': os.environ['AWS_EXECUTION_ENV'],
        'lang': os.environ['LANG']
    }
    
    return {
        "statusCode": 200,
        "body": json.dumps(env_var_dict)
    }
