import os
import redis
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ft_trans.settings")

# app: Celery = Celery("ft_trans")
password = getattr(settings, "REDIS_PASSWORD", None)
app = redis.Redis(
    host="redis",
    port=6379,
    password=password,
    ssl=True,
    ssl_cert_reqs="none",
)


# app.config_from_object("django.conf:settings", namespace="CELERY")  # type: ignore
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)  # type: ignore
