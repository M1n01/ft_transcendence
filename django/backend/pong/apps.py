from django.apps import AppConfig


class PongConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pong"

    def ready(self):
        import pong.signals

        # Black対策
        print(f"f{pong.signals}")
