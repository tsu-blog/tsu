import json
from src.util import service_mesh
from src.core.posts import listing

def handler(event, context):

    body = {
        "posts": listing.list_posts()
    }

    return {
        "statusCode": 200,
        "body": json.dumps(body)
    }
