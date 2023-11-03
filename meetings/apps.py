from django.apps import AppConfig


class MeetingsConfig(AppConfig):
    name = 'meetings'

    def ready(self):
        from meetings import updater 
        updater.start()
