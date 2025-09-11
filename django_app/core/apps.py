# from django.apps import AppConfig


# class CoreConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'core'

from django.apps import AppConfig

class CoreConfig(AppConfig):
    name = 'core'
    # name = '_django_mosquitto_client'
    def ready(self):
        from . import mqtt_client
        mqtt_client.run()