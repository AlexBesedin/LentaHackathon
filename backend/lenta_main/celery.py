import os
import sys
from celery import Celery

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'backend'))

from ml import tasks 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lenta_main.settings')


app = Celery('lenta_main')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
