import json
from src.util import service_mesh

def handler(event, context):

    body = {
        "posts": service_mesh.call('core-posts-listing')
    }

    return {
        "statusCode": 200,
        "body": json.dumps(body)
    }
