import os
from celery import Celery

os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

celery_app = Celery('core')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()

task = celery_app.task
