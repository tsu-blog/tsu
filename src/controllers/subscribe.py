from src.util import templates
from src.services import email_service, captcha_service
from urllib.parse import parse_qs
from src.util.config import ConfigValues
import base64

def handler(event, context):
    html = templates.render('subscribe.html', {})

    return {
        'statusCode': 200,
        'body': html,
        'headers': {
            'Content-Type': "text/html",
            'Cache-Control': f'max-age={ConfigValues.CACHE_TTL}',

        }
    }

def add_subscription(event, context):
    """Subscribe a new user, including sending an email confirmation to the user
    and a notification to the app owner"""

    # Extract relevant user details
    data = parse_qs(base64.b64decode(event['body']).decode('utf-8'))
    email = data.get('email')[0] if data.get('email') else None
    recaptcha_response = data.get('g-recaptcha-response')[0] if data.get('g-recaptcha-response') else None

    ret_data = {}
    if not captcha_service.verify(recaptcha_response):
        ret_data = {
            "error": f"Something went wrong verifying your identity. Try refreshing the page, or email us at {ConfigValues.CONTACT_EMAIL}."
        }
    else:
        try:
            email_service.add_subscription(email)
            ret_data = {
                "message": f"{email} successfully added to the subscriber list! You should receive an email confirmation shortly."
            }
        except Exception as e:
            print(e)
            ret_data = {
                "error": f"Something went wrong. Try refreshing the page, or email us at {ConfigValues.CONTACT_EMAIL}."
            }

    html = templates.render('subscribe.html', ret_data)

    return {
        'statusCode': 200,
        'body': html,
        'headers': {
            'Content-Type': "text/html"
        }
    }
