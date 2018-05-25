from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

if os.environ.get('ENV') in ['prod', 'worker']:
    module_path = 'config.settings.production'
else:
    module_path = 'config.settings.local'

app = Celery('mitra')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', module_path)
app.config_from_object(module_path, namespace='CELERY')


app.config_from_object('config.settings.local', namespace='CELERY')
app.autodiscover_tasks()
