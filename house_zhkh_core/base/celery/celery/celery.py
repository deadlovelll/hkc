import os

from house_zhkh_core.base.celery.celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'house_zhkh_core.settings.settings')

app = Celery('house_zhkh_core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()