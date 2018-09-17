import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('wine_gallery')
app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'daily-bill': {
        'task': 'tasks.bill',
        'schedule': crontab(hour=12, minute=0),
    },
    'daily-recommendation': {
        'task': 'tasks.generate_recommendations',
        'schedule': crontab(hour=12, minute=0),
    },
}
