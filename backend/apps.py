from django.apps import AppConfig
from django.db.models.signals import post_save


class BackendConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "backend"

    def ready(self):
        from backend import signals
