from src.util import templates
from src.services import email_service
from urllib.parse import parse_qs
from src.util.config import ConfigValues
import base64

def handler(event, context):
    html = templates.render('unsubscribe.html', {
        "email": event.get('queryStringParameters',{}).get('email')
    })

    return {
        'statusCode': 200,
        'body': html,
        'headers': {
            'Content-Type': "text/html",
            'Cache-Control': f'max-age={ConfigValues.CACHE_TTL}',
        }
    }

def remove_subscription(event, context):
    """Unsubscribes a user"""

    # Extract relevant user details
    data = parse_qs(base64.b64decode(event['body']).decode('utf-8'))
    email = data.get('email')[0] if data.get('email') else None

    ret_data = {}
    try:
        email_service.remove_subscription(email)
        ret_data = {
            "message": f"{email} has been removed from the subscriber list."
        }
    except Exception as e:
        print(e)
        ret_data = {
            "error": f"Something went wrong. Try refreshing the page, or email us at {ConfigValues.CONTACT_EMAIL}."
        }

    html = templates.render('unsubscribe.html', ret_data)

    return {
        'statusCode': 200,
        'body': html,
        'headers': {
            'Content-Type': "text/html"
        }
    }
