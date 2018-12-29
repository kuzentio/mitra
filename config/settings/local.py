from .base import *  # noqa

from dotenv import load_dotenv
from pathlib import Path  # python3 only

env_path = Path('.') / '.env.local'
load_dotenv(dotenv_path=str(env_path.absolute()))

DEBUG = True

AUTH_PASSWORD_VALIDATORS = []

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = ['localhost', '127.0.0.1']

INSTALLED_APPS += (
    'django_extensions',
    'debug_toolbar',
)

USE_TZ = False
