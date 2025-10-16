import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from django.http import HttpResponse
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync # channel group için
from asgiref.sync import sync_to_async
from app_monitor.models import Temperature,Device,Event,Alarm
from channels.db import database_sync_to_async
from urllib.parse import parse_qs # url query parametrelerini parse etmek için 250916
import traceback # Hata detaylarını (traceback dahil) görmek için:
import json
from django.utils import timezone
import datetime

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
# MQTT_TOPIC = "deneme_aaa"  # Göndereceğiniz konu adı
# MQTT_TOPIC = f"cihaz_{}"  # Göndereceğiniz konu adı
# MQTT_TOPIC = "cihaz_#"  # Göndereceğiniz konu adı
# MQTT_TOPIC = "cihaz_+"  # Göndereceğiniz konu adı
MQTT_TOPIC = "cihaz/+"  # Göndereceğiniz konu adı


client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("MQTT connected with result code " + str(rc))
    # client.subscribe("test/topic")
    # client.subscribe("deneme_aaa")
    # client.subscribe("cihaz_tum")
    client.subscribe(MQTT_TOPIC)
    print(f"cihaz/+ topice abone olundu...")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        payload_dict=json.loads(payload)
        payload_dict_type=payload_dict["type"]
        print(f"payload_dict_type: {payload_dict_type}")
        print(f"MQTT mesajı alındı: {payload}")
        # if "CONNECTION_BRW" in payload_dict:
        if payload_dict_type == "CONNACK_MQTT_BRW":
            device_id= payload_dict["xid"]
            print(f"msg.payload: {msg.payload}, type: {type(msg.payload)}")
            print(f"device_id mqtt on_message: {device_id}")


            grup_adı=f"esp_group_{device_id}"
            # WebSocket'e mesaj gönder (tüm bağlantılara) MQTT-----------> WEBSOCKET BROWSER
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
            # sync_to_async(channel_layer.group_send)(
            # "mqtt_group", # grup adı
            grup_adı, # grup adı
            {
            # "type": "send.mqtt", # WebSocket consumer'da tanımlı method
            # "text": payload,
            'type': 'group_message',
                    # 'message': message
            'message': payload
            },
            )
        if payload_dict_type == "CONN_ESP":
            device_id= payload_dict["xid"]
            device_id_obj=Device.objects.get(device_id=device_id)
            alarm_kesinti_object=Alarm.objects.get(alarm_id=1)
            try:
                print(f"connect try, device_id={device_id}")
                device_ip=payload_dict["xip"]
                # device_ip=payload_dict["xipppppppppppp"]
                device_name=payload_dict["xname"]
                device_port=payload_dict["xport"]
                temperature=payload_dict["xtemp"]
                humidity=payload_dict["xhum"]
                volt=payload_dict["xvolt"]
                xi00=payload_dict["xi00"]
                xi01=payload_dict["xi01"]
                xi02=payload_dict["xi02"]
                xi03=payload_dict["xi03"]
                xo0=payload_dict["xo0"]
                xo00=payload_dict["xo00"]
                xo01=payload_dict["xo01"]
                xo02=payload_dict["xo02"]
                xo03=payload_dict["xo03"]

                device_obj, created = Device.objects.update_or_create(
                    # email='test@example.com',
                    device_id=f"{device_id}",
                    defaults={
                        "device_name": f"{device_name}",
                        "device_ip": f"{device_ip}",
                        "device_port": f"{device_port}",
                    }
                )
                print(f"güncellenen cihaz nesnesi: {device_obj}, yeni cihaz mı: {created}")
                # device_id_conn=Device.objects.get(device_id=device_id)
                # device_id=Device.objects.get)(device_id=device_id) 
                event_all_clear=Event.objects.filter(event_active=True,device_id=device_id_obj,alarm_id=alarm_kesinti_object) # clear olmayan aynı alarm id li hatalı eventlar varsa hepsini clear yapar.
                for event in event_all_clear: 
                    event.event_active=False
                    event.finish_time=datetime.datetime.now()
                    event.save()

                # newRecord = Temperature)(temperature=temperature,humidity= humidity,volcum=volt, date=timezone.now(),device_name=device_name,device_id=device_id,input0=xi00,input1=xi01,input2=xi02,input3=xi03) #250610
                newRecord = Temperature(temperature=temperature,humidity= humidity,volcum=volt, date=timezone.now(),device_name=device_name,device_id=device_id_obj,input00=xi00,input01=xi01,input02=xi02,input03=xi03,cikis0=xo0,cikis00=xo00,cikis01=xo01,cikis02=xo02,cikis03=xo03) #250610

                newRecord.save() # CONNECTION TEMP kaydı
                print(f"newRecord: {newRecord}")
            except Exception as e:
                print(f"conn_esp device: {device_id} için event,temperature kaydı oluşamadı")
                print(f"Exception cinsi: {str(e)}")
                traceback.print_exc() # Hata detaylarını (traceback dahil) görmek için:
        
        if payload_dict_type == "PERYODIK":
            device_id= payload_dict["xid"]
            device_id_obj=Device.objects.get(device_id=device_id)
            device_name=payload_dict["xname"]
            device_port=payload_dict["xport"]
            temperature=payload_dict["xtemp"]
            humidity=payload_dict["xhum"]
            volt=payload_dict["xvolt"]
            xi00=payload_dict["xi00"]
            xi01=payload_dict["xi01"]
            xi02=payload_dict["xi02"]
            xi03=payload_dict["xi03"]
            xo0=payload_dict["xo0"]
            xo00=payload_dict["xo00"]
            xo01=payload_dict["xo01"]
            xo02=payload_dict["xo02"]
            xo03=payload_dict["xo03"]
            # device_id_socket=Device.objects.get(device_id=1)
            # newRecord = Temperature(temperature=16,humidity=44 ,volcum=11, date=timezone.now(),device_name="Test",device_id=device_id_socket) #250610
            # newRecord = Temperature(temperature=16,humidity=44 ,volcum=11, date=timezone.now(),device_name=device_name_socket,device_id=device_id_socket) #250610
            # newRecord = await sync_to_async(Temperature)(temperature=temperature_socket,humidity= humidity_socket,volcum=volt_socket, date=timezone.now(),device_name=device_name_socket,device_id=device_id_socket) #250610
            newRecord = Temperature(temperature=temperature,humidity= humidity,volcum=volt, date=timezone.now(),device_name=device_name,device_id=device_id_obj,input00=xi00,input01=xi01,input02=xi02,input03=xi03,cikis0=xo0,cikis00=xo00,cikis01=xo01,cikis02=xo02,cikis03=xo03) #250610
            newRecord.save()
            print(f"newRecord: {newRecord}")
            # self.send(text_data=json.dumps({"message": message}))
            # self.send(text_data=json.dumps({"message": str(timezone.now())}))
            # self.send(text_data=json.dumps({"message": str(timezone.localtime())}))
            # self.send(text_data=json.dumps({"message": f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ve deger:{text_data} '}))

        print(f"on_message msg: {msg}")
        print(f"on_message msg.payload: {msg.payload}")
        print(f"on_message msg.payload.decode.loads() dictionary: {json.loads(msg.payload.decode('utf-8'))}")
        print(f"Received message: {msg.payload.decode('utf-8')} on topic {msg.topic}")
        # return HttpResponse(f"Received message: {msg.payload.decode()} on topic {msg.topic}")
    except Exception as e:
        print(f"mqtt on_message exception: {str(e)}")

def run():
    #client = mqtt.Client() # client yukarıda global nesneye dönüştü,bu şekilde consumer.py de erişebiliriz... 251014
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