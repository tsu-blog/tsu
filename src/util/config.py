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

    CDN_BASE = config('TSU_CDN_BASE', 'https://my.blog')

    DEPLOYMENT_ID = config('TSU_DEPLOYMENT_ID', '')

    DEBUG = config('TSU_DEBUG', False, cast=bool)

    TEMPLATE = config('TSU_TEMPLATE', 'professional')

    POSTS_BUCKET = config('TSU_POSTS_BUCKET', 'tsu-dev-posts')

    PREFIX = config('TSU_PREFIX', 'tsu-dev-')

    HOMEPAGE = config('TSU_HOMEPAGE', 'https://my.blog')

    TITLE = config('TSU_TITLE', 'My Blog')

    DESCRIPTION = config('TSU_DESCRIPTION', 'My blog about my life.')

    AUTHOR = config('TSU_AUTHOR', 'FirstName LastName')