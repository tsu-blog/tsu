from src.util import templates
from src.services import post_service

def sitemap(event, context):
    posts = post_service.list_posts()

    html = templates.render('seo/sitemap.xml', {
        'posts': posts,
    })

    return {
        'statusCode': 200,
        'body': html,
        'headers': {
            'Content-Type': "text/xml"
        }
    }

def robots(event, context):
    html = templates.render('seo/robots.txt', {})
    
    return {
        'statusCode': 200,
        'body': html,
        'headers': {
            'Content-Type': "text/plain"
        }
    }
