# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/app_monitor/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
    re_path(r"ws/app_monitor_2/esp8266/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]