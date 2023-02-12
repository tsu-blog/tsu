from src.util import templates
from src.util.config import ConfigValues

def handler(event, context):
    html = templates.render('about.html', {})

    return {
        'statusCode': 200,
        'body': html,
        'headers': {
            'Content-Type': "text/html",
            'Cache-Control': f'max-age={ConfigValues.CACHE_TTL}',
        }
    }
