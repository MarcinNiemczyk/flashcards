from django.apps import AppConfig
from django.db.models.signals import post_save


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self):
        from api import signals
