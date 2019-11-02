import json
from src.services import post_service

def list(event, context):
    posts = post_service.list_posts()

    # Convert datetime objects into strings so json serialization works
    for post in posts:
        post['created_at'] = post['created_at'].strftime('%Y-%m-%d %H:%M:%S'),

    body = {
        "posts": posts
    }

    return {
        "statusCode": 200,
        "body": json.dumps(body)
    }
