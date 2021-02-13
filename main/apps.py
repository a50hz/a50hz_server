from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'
    def ready(self):
        from main.schelduler import scheduler
        scheduler.start()
