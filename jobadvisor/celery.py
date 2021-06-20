"""JObAdvisor celery."""
import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jobadvisor.settings")

app = Celery("JobAdvisor")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
