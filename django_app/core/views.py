from django.shortcuts import render
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
from .mqtt_client import send_message
from django.http import JsonResponse
import datetime


# Create your views here.
def mqtt_index(request):
    return render(request,"index.html")

def mqtt_publish(request):
    print("mqtt_publish girdi...")
    publish.single("test/topic", "djangodan gönderilen mesaj bu...", hostname="localhost", port=1883)

def send_mqtt_message(request):
    # message = "Django'dan MQTT'ye gelen mesaj "+ str(datetime.datetime.now())
    message = "Django'dan MQTT'ye gelen mesaj "+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    send_message(message)  # MQTT mesajını gönder
    return JsonResponse({"status": "Message sent successfully"})