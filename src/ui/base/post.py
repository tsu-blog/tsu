from src.util import templates
from src.core import posts

def handler(event, context):
    return {
        'statusCode': 200,
        'body': templates.render('post.html', {
            'post': posts.get_post(event['pathParameters']['id']),
        }),
        'headers': {
            'Content-Type': "text/html"
        }
    }
