from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

if os.environ.get('ENV') in ['prod', 'worker']:
    module = 'config.settings.production'
else:
    module = 'config.settings.local'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
