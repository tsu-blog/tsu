from src.util import templates
from src.services import post_service

def handler(event, context):
    return {
        'statusCode': 200,
        'body': templates.render('post.html', {
            'post': post_service.get_post(event['pathParameters']['id']),
        }),
        'headers': {
            'Content-Type': "text/html"
        }
    }
