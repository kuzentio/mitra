

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

# MIDDLEWARE += (
#     'django_pdb.middleware.PdbMiddleware',
# )
