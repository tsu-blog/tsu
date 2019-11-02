from src.util import templates
from src.services import post_service

def handler(event, context):
    return {
        'statusCode': 200,
        'body': templates.render('home.html', {
            'posts': post_service.list_posts(),
        }),
        'headers': {
            'Content-Type': "text/html"
        }
    }
