

from .base import *  # noqa

AUTH_PASSWORD_VALIDATORS = []


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mitra',
        'USER': 'igor',
        'PASSWORD': '',
        'HOST': 'localhost',
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

INSTALLED_APPS += (
    'django_extensions',
    # 'django_pdb',
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
