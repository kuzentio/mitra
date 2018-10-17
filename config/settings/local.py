from .base import *  # noqa

AUTH_PASSWORD_VALIDATORS = []

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = ['localhost', '127.0.0.1']

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS += [
    os.path.join(BASE_DIR, '..', 'node_modules'),
]

INSTALLED_APPS += (
    'django_extensions',
    'debug_toolbar',
)

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

MITRA_DUMMY_BITTREX_API_KEY = os.environ.get('MITRA_DUMMY_BITTREX_API_KEY')
MITRA_DUMMY_BITTREX_API_SECRET = os.environ.get('MITRA_DUMMY_BITTREX_API_SECRET')

BOOTSTRAP4 = {
    'jquery_url': STATIC_URL + 'jquery/dist/jquery.js',
    'base_url': STATIC_URL + 'bootstrap/',
    'css_url': STATIC_URL + 'bootstrap/dist/css/bootstrap.css',
    'theme_url': None,
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

BOOTSTRAP_BASE_URL = '/static/bootstrap/'
