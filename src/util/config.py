################################################################################
# TSU CONFIGURATION FILE
################################################################################
from decouple import AutoConfig, Csv

# Setup our config reader. Looks up keys with the following precedence
# 1. From host's env
# 2. From .env file in the project root (/tsu/src/.env)
# 3. From the default values provided below
config = AutoConfig(search_path='../')

class ConfigValues(object):
    APP_NAME = config('TSU_APP_NAME', 'tsu.main')
    DEPLOYMENT_ID = config('TSU_DEPLOYMENT_ID', '')
    DEBUG = config('TSU_DEBUG', False, cast=bool)

    POSTS_BUCKET = config('TSU_POSTS_BUCKET', 'tsu-dev-posts')
    CDN_BUCKET = config('TSU_CDN_BUCKET', 'tsu-dev-static')
    PREFIX = config('TSU_PREFIX', 'tsu-dev-')

    CDN_BASE = config('TSU_CDN_BASE', 'https://my.blog')
    TEMPLATE = config('TSU_TEMPLATE', 'professional')
    CACHE_TTL = config('TSU_CACHE_TTL', 60, cast=int)

    HOMEPAGE = config('TSU_HOMEPAGE', 'https://my.blog')
    DOMAIN = config('TSU_DOMAIN', 'my.blog')

    TITLE = config('TSU_TITLE', 'My Blog')
    DESCRIPTION = config('TSU_DESCRIPTION', 'My blog about my life.')
    AUTHOR = config('TSU_AUTHOR', 'FirstName LastName')

    SUBSCRIBER_TABLE = config('TSU_SUB_TABLE_NAME', '')
    SUB_CONFIRM_BCC = config('TSU_SUB_CONFIRM_BCC', '')
    RECAPTCHA_SECRET = config('TSU_RECAPTCHA_SECRET', '')
    CONTACT_EMAIL = config('TSU_CONTACT_EMAIL', 'hello@my.blog')

