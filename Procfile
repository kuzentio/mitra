web: gunicorn conf.wsgi
worker: celery -A mitra worker
beat: celery -A mitra beat --scheduler django_celery_beat.schedulers:DatabaseScheduler
