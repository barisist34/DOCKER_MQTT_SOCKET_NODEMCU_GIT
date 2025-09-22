# from django.apps import AppConfig


# class CoreConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'core'

from django.apps import AppConfig
import sys # makemigrations için eklendi 250921

class CoreConfig(AppConfig):
    name = 'core'
    # name = '_django_mosquitto_client'
    def ready(self):
        if 'runserver' in sys.argv: # makemigrations için eklendi 250921, sadece manage.py runserver çalışınca mqtt çalışacak.
            from . import mqtt_client # bu şekilde manage.py makemigrations komutunda hata alınmayacak... 
            mqtt_client.run() # HATA: socket.gaierror: [Errno 11001] getaddrinfo failed (client.connect("mosquitto", 1883, 60) kaynaklı)