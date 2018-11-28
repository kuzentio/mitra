from __future__ import absolute_import, unicode_literals
import os

import django
from celery import Celery

if os.environ.get('ENV') is not None:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.{}'.format(os.environ.get('ENV')))
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

django.setup()

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
