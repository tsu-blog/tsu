from src.util import templates
from src.services import post_service

def sitemap(event, context):
    return {
        'statusCode': 200,
        'body': templates.render('seo/sitemap.xml', {
            'posts': post_service.list_posts(),
        }),
        'headers': {
            'Content-Type': "text/xml"
        }
    }

def robots(event, context):
    return {
        'statusCode': 200,
        'body': templates.render('seo/robots.txt', {
        }),
        'headers': {
            'Content-Type': "text/plain"
        }
    }
