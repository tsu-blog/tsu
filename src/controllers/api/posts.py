import json
from src.services import posts

def list(event, context):

    body = {
        "posts": posts.list_posts()
    }

    return {
        "statusCode": 200,
        "body": json.dumps(body)
    }
