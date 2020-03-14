from src.util import templates
from src.services import post_service
from email import utils

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
            'Content-Type': "application/rss+xml"
        }
    }
