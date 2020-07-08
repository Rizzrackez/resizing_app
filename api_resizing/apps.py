from django.apps import AppConfig


class ApiResizingConfig(AppConfig):
    name = 'api_resizing'

    def ready(self):
         import api_resizing.signals

