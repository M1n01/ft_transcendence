import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ft_trans.settings")

app: Celery = Celery("ft_trans")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.timezone = "UTC"

# celery-beatの設定
app.conf.beat_schedule = {
    "run-every-hour-at-15-minutes": {
        "task": "tournament.tasks.close_application",
        "schedule": crontab(minute="10, 25, 40, 55"),
    },
}
