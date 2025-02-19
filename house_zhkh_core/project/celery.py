import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings.settings')

app = Celery('house_zhkh_core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()