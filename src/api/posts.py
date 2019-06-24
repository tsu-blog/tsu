import json
from src.core import posts

def list(event, context):

    body = {
        "posts": posts.list_posts()
    }

    return {
        "statusCode": 200,
        "body": json.dumps(body)
    }
