from src.util import templates
from src.services import image_service
import base64
from src.util.config import ConfigValues

def handler(event, context):
    image_url = event.get('queryStringParameters',{}).get('l')

    body, content_type = image_service.get_image(image_url)
    return {
        'statusCode': 200,
        'body': base64.b64encode(body).decode('utf-8'),
        'isBase64Encoded': True,
        'headers': {
            'Content-Type': content_type,
            'Cache-Control': f'max-age={ConfigValues.CACHE_TTL}',
        },
    }
