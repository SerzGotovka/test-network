import os
from celery import Celery
from django.conf import settings


import redis

redis = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD or None,
        decode_responses=True,
        charset="utf-8",
    )
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'electro.settings')

app = Celery("electro")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()