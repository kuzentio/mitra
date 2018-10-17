from .base import *  # noqa

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['*', ]

INSTALLED_APPS += (
    'gunicorn',
)
