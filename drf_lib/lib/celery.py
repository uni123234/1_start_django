from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drf_lib.settings")

app = Celery("lib")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
