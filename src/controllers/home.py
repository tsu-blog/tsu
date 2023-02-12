from src.util import templates
from src.services import post_service
from src.util.config import ConfigValues

def handler(event, context):
    posts = post_service.list_posts()

    html = templates.render('home.html', {
        'posts': posts,
    })

    return {
        'statusCode': 200,
        'body': html,
        'headers': {
            'Content-Type': "text/html",
            'Cache-Control': f'max-age={min(ConfigValues.CACHE_TTL,10*60)}', # Max TTL 10 min
        }
    }
