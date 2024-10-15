import os
import redis
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ft_trans.settings")

# app: Celery = Celery("ft_trans")
password = getattr(settings, "REDIS_PASSWORD", None)
ssl = getattr(settings, "REDIS_SSL", None)
port = getattr(settings, "REDIS_PORT", None)
app = redis.Redis(
    host="redis",
    port=port,
    password=password,
    ssl=ssl,
    ssl_cert_reqs="none",
)


# app.config_from_object("django.conf:settings", namespace="CELERY")  # type: ignore
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)  # type: ignore
