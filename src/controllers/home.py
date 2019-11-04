from src.util import templates
from src.services import post_service

def handler(event, context):
    posts = post_service.list_posts()

    html = templates.render('home.html', {
        'posts': posts,
    })
    
    return {
        'statusCode': 200,
        'body': html,
        'headers': {
            'Content-Type': "text/html"
        }
    }
