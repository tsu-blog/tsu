from src.util import templates
from src.services import post_service

def handler(event, context):
    post = post_service.get_post(event['pathParameters']['id'])

    html = templates.render('post.html', {
        'post': post
    })
    return {
        'statusCode': 200,
        'body': html,
        'headers': {
            'Content-Type': "text/html"
        }
    }
