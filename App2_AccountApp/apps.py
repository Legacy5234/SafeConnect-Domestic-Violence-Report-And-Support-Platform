from django.apps import AppConfig


class App2AccountappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'App2_AccountApp'

    def ready(self):
        import App2_AccountApp.signals
