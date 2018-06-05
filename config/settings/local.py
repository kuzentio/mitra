from .base import *  # noqa

AUTH_PASSWORD_VALIDATORS = []

# SECRET_KEY = 'SDFSDFD'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
    }
}


STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, '..', 'static'),
]
STATIC_URL = '/static/'

INSTALLED_APPS += (
    'django_extensions',
)

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework_datatables.renderers.DatatablesRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_datatables.filters.DatatablesFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework_datatables.pagination.DatatablesPageNumberPagination',
    'PAGE_SIZE': 50,
}

SHELL_PLUS_POST_IMPORTS = (
    ('apps.order.factories', '*'),
    ('apps.profile_app.factories', '*'),
    ('apps.order.tasks', '*')
)

USE_TZ = False

# Celery application definition
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'

CELERY_RESULT_BACKEND = 'django-db'


MITRA_DUMMY_BITTREX_API_KEY = '992ba48612564b72af9757afdf444121'  # TODO: required
MITRA_DUMMY_BITTREX_API_SECRET = 'a9eb1d61422b4b8a9253e20949be66d5'  # TODO: required
