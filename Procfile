web: gunicorn --bind :8000 core.settings.wsgi:application

celery_worker: celery worker -A core.settings.celery.app -B -l INFO
celery_beat: celery -A core beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler