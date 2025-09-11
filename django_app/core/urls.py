from django.contrib import admin
from django.urls import path
from .views import mqtt_index,send_mqtt_message

urlpatterns = [
    path('', mqtt_index,name="mqtt_index"),
    path('send_mqtt_message', send_mqtt_message,name="send_mqtt_message"),
]
