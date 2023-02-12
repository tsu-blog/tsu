from src.util import templates
from src.services import post_service
from email import utils
from src.util.config import ConfigValues

def handler(event, context):
    posts = post_service.list_posts()

    xml = templates.render('rss.xml', {
        'posts': posts,
        'date_format': utils.format_datetime
    })

    return {
        'statusCode': 200,
        'body': xml,
        'headers': {
            'Content-Type': "application/rss+xml",
            'Cache-Control': f'max-age={min(ConfigValues.CACHE_TTL,60*60)}', # Max TTL 60 min
        }
    }
