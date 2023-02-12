import requests
from util.config import ConfigValues

def verify(recaptcha_response):
    resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data={
        'secret': ConfigValues.RECAPTCHA_SECRET,
        'response': recaptcha_response,
    })

    data = resp.json()

    if not data.get('success'):
        return False

    # Users get scored on a range of 0-1 (0 = bot, 1 = real)
    return data.get('score') > 0.5
