from src.util import templates
from src.services import post_service
from src.util.config import ConfigValues

def sitemap(event, context):
    posts = post_service.list_posts()

    html = templates.render('seo/sitemap.xml', {
        'posts': posts,
    })

    return {
        'statusCode': 200,
        'body': html,
        'headers': {
            'Content-Type': "text/xml",
            'Cache-Control': f'max-age={min(ConfigValues.CACHE_TTL,24*60*60)}', # Max TTL 1 day
        }
    }

def robots(event, context):
    html = templates.render('seo/robots.txt', {})

    return {
        'statusCode': 200,
        'body': html,
        'headers': {
            'Content-Type': "text/plain",
            'Cache-Control': f'max-age={min(ConfigValues.CACHE_TTL,24*60*60)}', # Max TTL 1 day
        }
    }
