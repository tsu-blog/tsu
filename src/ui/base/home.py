from src.util import templates
from src.core import posts

def handler(event, context):
    return {
        'statusCode': 200,
        'body': templates.render('home.html', {
            'posts': posts.list_posts(),
        }),
        'headers': {
            'Content-Type': "text/html"
        }
    }
