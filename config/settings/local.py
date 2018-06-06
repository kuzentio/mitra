from .base import *  # noqa

AUTH_PASSWORD_VALIDATORS = []

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

BOOTSTRAP4 = {
    # 'jquery_url': '//code.jquery.com/jquery.min.js',
    'jquery_url': STATIC_URL + 'jquery/dist/jquery.js',
    # 'base_url': '//maxcdn.bootstrapcdn.com/bootstrap/3.3.7/',
    'base_url': STATIC_URL + 'bootstrap/',
    # 'css_url': None,
    'css_url': STATIC_URL + 'bootstrap/dist/css/bootstrap.css',
    'theme_url': None,
    # 'theme_url': STATIC_URL + 'bootstrap/dist/css/bootstrap-theme.css',
    # 'javascript_url': None,
    'javascript_url': STATIC_URL + 'bootstrap/dist/js/bootstrap.js',
    'javascript_in_head': False,
    'include_jquery': False,
    'horizontal_label_class': 'col-md-3',
    'horizontal_field_class': 'col-md-9',
    'set_placeholder': True,
    'required_css_class': '',
    'error_css_class': 'has-error',
    'success_css_class': 'has-success',
    'formset_renderers': {
        'default': 'bootstrap4.renderers.FormsetRenderer',
    },
    'form_renderers': {
        'default': 'bootstrap4.renderers.FormRenderer',
    },
    'field_renderers': {
        'default': 'bootstrap4.renderers.FieldRenderer',
        'inline': 'bootstrap4.renderers.InlineFieldRenderer',
    },
}

#  EXAMPLE
# BOOTSTRAP3 = {
#     'include_jquery': False,
#     'jquery_url': '/static/jquery.min.js',
#     'base_url': '/static/bootstrap/',
#     'css_url': '/static/bootstrap/css/bootstrap.min.css',
#     'theme_url': '/static/bootstrap/css/bootstrap-theme.min.css',
#     'javascript_url': '/static/bootstrap/js/bootstrap.min.js',
# }
BOOTSTRAP_BASE_URL = '/static/bootstrap/'
