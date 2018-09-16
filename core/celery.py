import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('wine_gallery')
app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()
