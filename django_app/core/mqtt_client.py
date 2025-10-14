# import paho.mqtt.client as mqtt

# def on_connect(client, userdata, flags, rc):
#     print("Connected with result code " + str(rc))
#     client.subscribe("test/topic")

# def on_message(client, userdata, msg):
#     print(f"Message received: {msg.payload.decode()}")

# client = mqtt.Client()
# client.on_connect = on_connect
# client.on_message = on_message

# client.connect("mosquitto", 1883, 60)
# client.loop_start()

################
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from django.http import HttpResponse
import json
# Mosquitto Broker Bilgileri
# MQTT_BROKER = "localhost"  # veya Mosquitto'nun IP adresi
# MQTT_BROKER = "172.19.0.1"  # veya Mosquitto'nun IP adresi
# MQTT_BROKER = "172.18.0.3"  # veya Mosquitto'nun IP adresi
MQTT_BROKER = "mosquitto"  # veya Mosquitto'nun IP adresi
# MQTT_BROKER = "192.168.43.10"  # veya Mosquitto'nun IP adresi
# MQTT_BROKER = "172.18.0.2"  # veya Mosquitto'nun IP adresi (PS C:\WINDOWS\system32> docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mosquitto)
MQTT_PORT = 1883  # Mosquitto'nun varsayılan portu
# MQTT_PORT = 1884  # Mosquitto'nun varsayılan portu
# MQTT_TOPIC = "test/topic"  # Göndereceğiniz konu adı
MQTT_TOPIC = "deneme_aaa"  # Göndereceğiniz konu adı

def on_connect(client, userdata, flags, rc):
    print("MQTT connected with result code " + str(rc))
    # client.subscribe("test/topic")
    client.subscribe("deneme_aaa")
    print(f"deneme_aaa topice abone olundu...")

def on_message(client, userdata, msg):
    try:
        print(f"on_message msg: {msg}")
        print(f"on_message msg.payload: {msg.payload}")
        print(f"on_message msg.payload.decode.loads() dictionary: {json.loads(msg.payload.decode('utf-8'))}")
        print(f"Received message: {msg.payload.decode('utf-8')} on topic {msg.topic}")
        # return HttpResponse(f"Received message: {msg.payload.decode()} on topic {msg.topic}")
    except Exception as e:
        print(f"mqtt on_message exception: {str(e)}")

def run():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("mosquitto", 1883, 60) # service adı ile bağlantı
    # client.connect("172.19.0.3", 1883, 60) # service adı ile bağlantı
    # client.connect("192.168.43.10", 1883, 60) # service adı ile bağlantı
    # client.connect("localhost", 1883, 60) # service adı ile bağlantı
    # client.connect("192.168.1.35", 1883, 60) # service adı ile bağlantı
    # client.connect("localhost", 1884, 60) # service adı ile bağlantı
    print("def run icinde client.connect gecti...")
    client.loop_start()
    print("def run icinde client.loop_start gecti...")
    # return HttpResponse("MQTT client is running.")
    # client.loop_forever()

# client = mqtt.Client()
# client.on_connect = on_connect
# client.on_message = on_message

# client.connect("localhost", 1883, 60)
# client.loop_forever()

# def run():
#     client = mqtt.Client()
#     client.on_connect = on_connect
#     client.on_message = on_message
#     # "mosquitto" docker servisi adı, containerlar arasında DNS olarak çalışır
#     client.connect("mosquitto", 1883, 60)
#     # client.loop_forever() main thread’i bloklar, o yüzden thread ile başlatıyoruz
#     thread = threading.Thread(target=client.loop_forever)
#     thread.daemon = True
#     thread.start()

# MQTT istemcisini başlatma
def create_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    return client

# Mesaj göndermek için bu fonksiyonu çağırabilirsiniz
def send_message(message):
    client = create_mqtt_client()
    client.loop_start()  # Asenkron işlem başlatma
    client.publish(MQTT_TOPIC, message)  # Buraya gönderilecek mesajı yazın
    client.loop_stop()  # İşlem durdurma