from .base import *  # noqa

import dj_database_url

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += (
    'gunicorn',
)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'ERROR'),
        },
    },
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_URL = '/static/'

MIDDLEWARE += [
    'whitenoise.middleware.WhiteNoiseMiddleware',
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

if not os.path.exists(os.path.join(BASE_DIR, 'node_modules')):
    os.makedirs(os.path.join(BASE_DIR, 'node_modules'))

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'node_modules'),
    os.path.join(BASE_DIR, 'static'),
]

# ALLOWED_HOSTS += ['dextra-test.herokuapp.com', ]

DATABASES['default'] = dj_database_url.config()
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

CELERY_BROKER_URL = CLOUDAMQP_URL = os.environ.get('CLOUDAMQP_URL')
