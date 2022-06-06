import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.timezone = 'Europe/London'


# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # 'bot_mercado_livre': {
    #     'task': 'apps.home.tasks.save_cars_mercado_livre',
    #     'schedule': 240.0,
    # },
    # 'bot_icarros': {
    #     'task': 'apps.home.tasks.save_icarros',
    #     'schedule': 240.0,
    # },
    'node': {
        'task': 'apps.home.tasks.node',
        'schedule': 900.0,
    },
}