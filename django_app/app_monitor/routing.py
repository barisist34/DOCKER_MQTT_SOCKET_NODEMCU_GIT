# chat/routing.py
from django.urls import re_path,path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/app_monitor/(?P<room_name>\w+)/$", consumers.MqttConsumer.as_asgi()),
    re_path(r"ws/app_monitor_2/esp8266/(?P<room_name>\w+)/$", consumers.MqttConsumer.as_asgi()),
    # re_path(r"ws/app_monitor_2/event_yenile/$", consumers.EventYenileConsumer.as_asgi()),
    # path("ws/app_monitor_2/esp8266/abc/"),

]