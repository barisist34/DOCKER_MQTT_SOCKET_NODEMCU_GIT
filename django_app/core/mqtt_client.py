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
# MQTT_BROKER = "mosquitto"  # veya Mosquitto'nun IP adresi
MQTT_BROKER = "192.168.1.35"  # veya Mosquitto'nun IP adresi
# MQTT_BROKER = "192.168.43.10"  # veya Mosquitto'nun IP adresi
# MQTT_BROKER = "172.18.0.2"  # veya Mosquitto'nun IP adresi (PS C:\WINDOWS\system32> docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mosquitto)
MQTT_PORT = 1883  # Mosquitto'nun varsayılan portu
# MQTT_PORT = 1884  # Mosquitto'nun varsayılan portu
# MQTT_TOPIC = "test/topic"  # Göndereceğiniz konu adı
# MQTT_TOPIC = "deneme_aaa"  # Göndereceğiniz konu adı
# MQTT_TOPIC = f"cihaz_{}"  # Göndereceğiniz konu adı
# MQTT_TOPIC = "cihaz_#"  # Göndereceğiniz konu adı
# MQTT_TOPIC = "cihaz_+"  # Göndereceğiniz konu adı
# MQTT_TOPIC = "cihaz/#"  # Göndereceğiniz konu adı ,, "cihaz/{device_id_scope}/BRW" gelmesin diye yoruma alındı
MQTT_TOPIC = "cihaz/+"
WILL_TOPIC="cihaz/+/status"

client = mqtt.Client() # mosquitto serverın clientı

def on_connect(client, userdata, flags, rc):
    print("MQTT connected with result code " + str(rc))
    # client.subscribe("test/topic")
    # client.subscribe("deneme_aaa")
    # client.subscribe("cihaz_tum")
    client.subscribe(MQTT_TOPIC)
    client.subscribe(WILL_TOPIC)
    print(f"cihaz/+ topice abone olundu...")

def on_disconnect(client, userdata, rc):
    print(f"client:{client}, Bağlantı kesildi. Kod:", rc)
    if rc != 0:
        print("Beklenmeyen bağlantı kesilmesi!")

def on_message(client, userdata, msg):
    """
    ***payload_dict_type[""] kontrolü:
    "CONNACK_MQTT_BRW" or "INPUTLAR_ESP" -- browser açılış veya esp input giriş
    "CIKISLAR_ESP" -- browserdan çıkış komutu,esp den gelen mesaj
    "CONN_ESP" -- esp ilk enerjilendiğinde gelen mesaj
    "PERYODIK" -- esp den 1dk peryotla gelen mesaj, Temperature database kayıt yapılır
    "willmesaj" -- esp kesildiğinde mosquittadan djangoya gelen mesaj
    "online" -- esp ayaktayken mosquitto kesildiğinde,mosquitto yeniden up olunca gelen mesaj
    "PWM_ACK"-- esp den gelen pwm dönüş mesajı
    """

    # try:
    payload = msg.payload.decode() # GLOBAL
    payload_dict=json.loads(payload) # GLOBAL
    payload_dict_type=payload_dict["type"] # GLOBAL
    print(f"payload_dict_type: {payload_dict_type}")
    print(f"MQTT mesajı alındı: {payload}")
    channel_layer = get_channel_layer() # bütün channel_layer.group_send de geçerli
    # if "CONNECTION_BRW" in payload_dict:
    if payload_dict_type == "CONNACK_MQTT_BRW" or payload_dict_type == "INPUTLAR_ESP":
        device_id= payload_dict["xid"]
        print(f"msg.payload: {msg.payload}, type: {type(msg.payload)}")
        print(f"device_id mqtt on_message: {device_id}")
        print(f"payload_dict['xid']: {payload_dict['xid']} ")

        grup_adı=f"esp_group_{device_id}"
        # WebSocket'e mesaj gönder (tüm bağlantılara) MQTT-----------> WEBSOCKET BROWSER
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

        if payload_dict_type == "INPUTLAR_ESP":
            ### INPUT EVENT OLUŞTURMA, CLEAR YAPMA
            try:
                device_id= payload_dict["xid"]
                input0=str(payload_dict['xi00'])
                print(f"input0:{input0}, type(input0):{type(input0)}")
                input1=str(payload_dict['xi01'])
                print(f"input1:{input1}, type(input1):{type(input1)}")
                input2=str(payload_dict['xi02'])
                print(f"input2:{input2}, type(input2):{type(input2)}")
                input3=str(payload_dict['xi03'])
                print(f"input3:{input3}, type(input3):{type(input3)}")
                input_no=str(payload_dict['xinput_id'])
                print(f"input_no:{input_no}, type(input_no):{type(input_no)}")
                device_id_int=int(payload_dict['xid'])
                device_obj=Device.objects.get(device_id=device_id_int)
                # device=Device.objects.get(device_id=json_socket_sid) #250615
                datetime_now=datetime.datetime.now() #250513
                alarm_kesinti_object=Alarm.objects.get(alarm_id=1)
                alarm_input0_object=Alarm.objects.get(alarm_id=7)
                # print(f"input0_active_event_available: {input0_active_event_available}")
                alarm_input0_object=Alarm.objects.get(alarm_id=7)
                input0_active_event_available=Event.objects.filter(alarm_id=alarm_input0_object).filter(event_active=True).filter(device_id=device_obj).count()
                alarm_input1_object=Alarm.objects.get(alarm_id=8)
                input1_active_event_available=Event.objects.filter(alarm_id=alarm_input1_object).filter(event_active=True).filter(device_id=device_obj).count()
                alarm_input2_object=Alarm.objects.get(alarm_id=9)
                input2_active_event_available=Event.objects.filter(alarm_id=alarm_input2_object).filter(event_active=True).filter(device_id=device_obj).count()
                alarm_input2_object=Alarm.objects.get(alarm_id=9)
                alarm_input3_object=Alarm.objects.get(alarm_id=10)
                input3_active_event_available=Event.objects.filter(alarm_id=alarm_input3_object).filter(event_active=True).filter(device_id=device_obj).count()
                if input0 or input1 or input2 or input3 == "1":
                    if input_no=="0" and  input0 == "1" and input0_active_event_available == 0:
                        new_input_event=Event(device_id=device_obj,device_name=device_obj.device_name,alarm_id=alarm_input0_object,alarm_name="Giriş--00 Aktif",start_time=datetime_now,event_active=True)
                        new_input_event.save()
                        print(f"new_input_event--1: f{new_input_event}")
                        # event_list_view()
                        # return redirect('/app_monitor/event_list_view') 
                        # redirect('/app_monitor/scheduler_cihaz')
                        print("redirect scheduler altı...")
                    if input_no=="1" and  input1 == "1" and input1_active_event_available == 0:
                        new_input_event=Event(device_id=device_obj,device_name=device_obj.device_name,alarm_id=alarm_input1_object,alarm_name="Giriş--01 Aktif",start_time=datetime_now,event_active=True)
                        new_input_event.save()
                        print(f"new_input_event--1: f{new_input_event}")
                        # redirect('/app_monitor/scheduler_cihaz')
                        print("redirect scheduler altı...")
                    if input_no=="2" and  input2 == "1" and input1_active_event_available == 0:
                        new_input_event=Event(device_id=device_obj,device_name=device_obj.device_name,alarm_id=alarm_input2_object,alarm_name="Giriş--02 Aktif",start_time=datetime_now,event_active=True)
                        new_input_event.save()
                        print(f"new_input_event--1: f{new_input_event}")
                        # redirect('/app_monitor/scheduler_cihaz')
                        print("redirect scheduler altı...")
                    if input_no=="3" and input3 == "1" and input3_active_event_available == 0:
                        new_input_event=Event(device_id=device_obj,device_name=device_obj.device_name,alarm_id=alarm_input3_object,alarm_name="Giriş--03 Aktif",start_time=datetime_now,event_active=True)
                        new_input_event.save()
                        print(f"new_input_event--1: f{new_input_event}")
                        # redirect('/app_monitor/scheduler_cihaz')
                        print("redirect scheduler altı...")
                if input_no=="0" and input0 == "0" and input0_active_event_available != 0: # alarm devam etmiyor ve aktif event varsa (count sayar)
                    print(f"input0 == 0 and input0_active_event_available !=0 girdi...")
                    event_all_clear=Event.objects.filter(event_active=True,alarm_id=alarm_input0_object,device_id=device_obj) # clear olmayan aynı alarm id li hatalı eventlar varsa hepsini clear yapar.
                    for event in event_all_clear: 
                        event.event_active=False
                        event.finish_time=datetime.datetime.now()
                        event.save()
                    print("event clear RETURN event_list_view////")
                    # return redirect('/app_monitor/scheduler_cihaz')
                    # redirect('/app_monitor/scheduler_cihaz')
                    print("redirect scheduler altı...clear")
                if input_no=="1" and input1 == "0" and input1_active_event_available != 0: # alarm devam etmiyor ve aktif event varsa (count sayar)
                    print(f"input1 == 0 and input1_active_event_available !=0 girdi...")
                    event_all_clear=Event.objects.filter(event_active=True,alarm_id=alarm_input1_object,device_id=device_obj) # clear olmayan aynı alarm id li hatalı eventlar varsa hepsini clear yapar.
                    for event in event_all_clear: 
                        event.event_active=False
                        event.finish_time=datetime.datetime.now()
                        # event.save)()
                        event.save()
                    print("event clear RETURN event_list_view////")
                    # return redirect('/app_monitor/scheduler_cihaz')
                    # redirect('/app_monitor/scheduler_cihaz')
                    print("redirect scheduler altı...clear")
                if input_no=="2" and input2 == "0" and input2_active_event_available != 0: # alarm devam etmiyor ve aktif event varsa (count sayar)
                    print(f"input2 == 0 and input2_active_event_available !=0 girdi...")
                    event_all_clear=Event.objects.filter(event_active=True,alarm_id=alarm_input2_object,device_id=device_obj) # clear olmayan aynı alarm id li hatalı eventlar varsa hepsini clear yapar.
                    for event in event_all_clear: 
                        event.event_active=False
                        event.finish_time=datetime.datetime.now()
                        event.save()
                    print("event clear RETURN event_list_view////")
                    # return redirect('/app_monitor/scheduler_cihaz')
                    # redirect('/app_monitor/scheduler_cihaz')
                    print("redirect scheduler altı...clear")
                if input_no=="3" and input3 == "0" and input3_active_event_available != 0: # alarm devam etmiyor ve aktif event varsa (count sayar)
                    print(f"input3 == 0 and input3_active_event_available !=0 girdi...")
                    event_all_clear=Event.objects.filter(event_active=True,alarm_id=alarm_input3_object,device_id=device_obj) # clear olmayan aynı alarm id li hatalı eventlar varsa hepsini clear yapar.
                    for event in event_all_clear: 
                        event.event_active=False
                        event.finish_time=datetime.datetime.now()
                        # event.save()
                        event.save()
                    print("event clear RETURN event_list_view////")
                #### IKINCI BIR GRUBA SOKET MESAJ GONDERME 
                async_to_sync(channel_layer.group_send)(
                "event_yenileme", # grup adı
                {
                # 'type': 'group_message',
                'type': 'yenile_mesaji',
                'message': "{'type':'event_yenileme'}"
                },
                )
            except Exception as e:
                print(f"EXCEPTION INPUTLAR_ESP device_id:{device_id} için exception: {str(e)}")
            ### INPUTLAR_ESP SONU

    if payload_dict_type == "CIKISLAR_ESP":
        device_id= payload_dict["xid"]
        print(f"msg.payload: {msg.payload}, type: {type(msg.payload)}")
        print(f"device_id mqtt on_message: {device_id}")


        grup_adı=f"esp_group_{device_id}"
        # WebSocket'e mesaj gönder (tüm bağlantılara) MQTT-----------> WEBSOCKET BROWSER
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
        #### IKINCI BIR GRUBA SOKET MESAJ GONDERME (CIKISLAR_ESP)
        async_to_sync(channel_layer.group_send)(
        "event_yenileme", # grup adı
        {
        # 'type': 'group_message',
        'type': 'yenile_mesaji',
        'message': "{'type':'event_yenileme'}"
        },
        )
    if payload_dict_type == "CONN_ESP": # esp ilk enerjilendiğinde gelen mesaj
        device_id= payload_dict["xid"]
        device_name=payload_dict["xname"]
        device_ip=payload_dict["xip"]
        device_port=payload_dict["xport"]
        try:
            # DATABASE de yoksa cihazı ekle, bilgi değiştiyse güncelle 
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
        except Exception as e:
            print(f"EXCEPTION device_id:{device_id} için CONN_ESP girişinde cihaz güncelle veya oluştur exception: {str(e)}")

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

            # device_id_conn=Device.objects.get(device_id=device_id)
            # device_id=Device.objects.get)(device_id=device_id) 
            event_all_clear=Event.objects.filter(event_active=True,device_id=device_id_obj,alarm_id=alarm_kesinti_object) # clear olmayan aynı alarm id li hatalı eventlar varsa hepsini clear yapar.
            for event in event_all_clear: 
                event.event_active=False
                event.finish_time=datetime.datetime.now()
                event.save()
                print(f"CLEAR EVENT CONN_ESP: {event}")

            # newRecord = Temperature)(temperature=temperature,humidity= humidity,volcum=volt, date=timezone.now(),device_name=device_name,device_id=device_id,input0=xi00,input1=xi01,input2=xi02,input3=xi03) #250610
            newRecord = Temperature(temperature=temperature,humidity= humidity,volcum=volt, date=timezone.now(),device_name=device_name,device_id=device_id_obj,input00=xi00,input01=xi01,input02=xi02,input03=xi03,cikis0=xo0,cikis00=xo00,cikis01=xo01,cikis02=xo02,cikis03=xo03) #250610

            newRecord.save() # CONNECTION TEMP kaydı
            print(f"newRecord: {newRecord}")

            #### IKINCI BIR GRUBA SOKET MESAJ GONDERME (CONN_ESP), kesinti alarmı düzelir
            async_to_sync(channel_layer.group_send)(
            "event_yenileme", # grup adı
            {
            # 'type': 'group_message',
            'type': 'yenile_mesaji',
            'message': "{'type':'event_yenileme'}"
            },
            )
        except Exception as e:
            print(f"EXCEPTION conn_esp device: {device_id} için event,temperature kaydı oluşamadı")
            print(f"Exception cinsi: {str(e)}")
            traceback.print_exc() # Hata detaylarını (traceback dahil) görmek için:
    
    if payload_dict_type == "PERYODIK":
        try: 
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
        except Exception as e:
            print(f"EXCEPTION PERYODIK device_id:{device_id} için exception: {str(e)}")

    if payload_dict_type == "willmesaj": # mosquitto ayakteyken esp kesilince,mosquittodan gelen mesaj,TOPIC:"cihaz/+/status"
        try:
                
            # device_id= payload_dict["device_id"]
            device_id= payload_dict["xid"]
            device_name= payload_dict["xname"]
            device_ip= payload_dict["xip"]
            device_port= payload_dict["xport"]        
            # DATABASE de yoksa cihazı ekle, bilgi değiştiyse güncelle 
            device_obj, created = Device.objects.update_or_create(
                # email='test@example.com',
                # device_id=f"{device_id}",
                device_id=f"{device_id}",
                defaults={
                    "device_name": f"{device_name}",
                    "device_ip": f"{device_ip}",
                    "device_port": f"{device_port}",
                }
            )
            print(f"güncellenen cihaz nesnesi: {device_obj}, yeni cihaz mı: {created}")

            device_id_obj=Device.objects.get(device_id=device_id)
            alarm_kesinti_object=Alarm.objects.get(alarm_id=1)
            print(f"cihaz kesildi wilmesajla alındı: {device_id}")
            new_outage_event=Event(device_id=device_id_obj,device_name=device_id_obj.device_name,alarm_id=alarm_kesinti_object,start_time=timezone.now(),event_active=True)
            new_outage_event.save()
            print(f"new_outage_event: {new_outage_event}")

        except Exception as e:
            print(f"EXCEPTION device_id: {device_id} için will kısım için exception: {str(e)}")

        #### IKINCI BIR GRUBA SOKET MESAJ GONDERME (willmesaj), kesinti alarmı oluşur
        async_to_sync(channel_layer.group_send)(
        "event_yenileme", # grup adı
        {
        # 'type': 'group_message',
        'type': 'yenile_mesaji',
        'message': "{'type':'event_yenileme'}"
        },
        )

    if payload_dict_type == "online_will": # mosquitto kesilince esp de kesikse,esp mosquittodan önce aktif olursa,
                                        # CONN_ESP de clear var, esp burada restart olmadığından, buradan clear gelmez. 
                                        # mosquitto yeniden up olunca esp type:online mesajı gönderir. TOPIC:"cihaz/+/status"
        try:
                
            # device_id= payload_dict["device_id"]
            device_id= payload_dict["xid"]
            device_name= payload_dict["xname"]
            device_ip= payload_dict["xip"]
            device_port= payload_dict["xport"]        
            # DATABASE de yoksa cihazı ekle, bilgi değiştiyse güncelle 
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

            device_id_obj=Device.objects.get(device_id=device_id)
            alarm_kesinti_object=Alarm.objects.get(alarm_id=1)
        
            event_all_clear=Event.objects.filter(event_active=True,device_id=device_id_obj,alarm_id=alarm_kesinti_object) # clear olmayan aynı alarm id li hatalı eventlar varsa hepsini clear yapar.
            for event in event_all_clear: 
                event.event_active=False
                event.finish_time=datetime.datetime.now()
                event.save()
                print(f"CLEAR EVENT online_reconnect: {event}")
        except Exception as e:
            print(f"EXCEPTION: device_id: {device_id} için online kısım event_all_clear için exception: {str(e)}")
        #### IKINCI BIR GRUBA SOKET MESAJ GONDERME
        async_to_sync(channel_layer.group_send)(
        "event_yenileme", # grup adı
        {
        'type': 'yenile_mesaji',
        'message': "{'type':'event_yenileme'}"
        },
        )

    if payload_dict_type == "PWM_ACK":
        device_id= payload_dict["xid"]
        device_id_obj=Device.objects.get(device_id=device_id)
        pwm_no=payload_dict["xpwm_no"]
        pwm_deger=payload_dict["xpwm_deger"]
        alarm_pwm_object=Alarm.objects.get(alarm_id=11)
        try:
            event_pwm_clear=Event.objects.filter(event_active=True,device_id=device_id_obj,alarm_id=alarm_pwm_object)
            for event in event_pwm_clear: # bu cihazda daha önceki pwm eventler clear yapılıyor
                event.event_active=False
                event.finish_time=datetime.datetime.now()
                event.save()
        except:
            print(f"device_id:{device_id} için aktif pwm eventi olmadığı için ilk pwm event aşağıda oluşturulacak...")
        new_pwm_event=Event(device_id=device_id_obj,device_name=device_id_obj.device_name,alarm_id=alarm_pwm_object,alarm_name=alarm_pwm_object.alarm_name,start_time=timezone.now(),event_active=True,info=f"PWM değeri:{pwm_deger}")
        new_pwm_event.save()
        print(f"new_pwm_event: {new_pwm_event}")

        #### IKINCI BIR GRUBA SOKET MESAJ GONDERME
        async_to_sync(channel_layer.group_send)(
        "event_yenileme", # grup adı
        {
        'type': 'yenile_mesaji',
        'message': "{'type':'event_yenileme'}"
        },
        )

    print(f"on_message msg: {msg}")
    print(f"on_message msg.payload: {msg.payload}")
    print(f"on_message msg.payload.decode.loads() dictionary: {json.loads(msg.payload.decode('utf-8'))}")
    print(f"Received message: {msg.payload.decode('utf-8')} on topic {msg.topic}")
    # return HttpResponse(f"Received message: {msg.payload.decode()} on topic {msg.topic}")
    # except Exception as e:
    #     print(f"device_id:{device_id} için mqtt on_message exception: {str(e)}")

def run():
    #client = mqtt.Client() # client yukarıda global nesneye dönüştü,bu şekilde consumer.py de erişebiliriz... 251014
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect=on_disconnect #def on_disconnect çalışabilmesi için
    # client.connect("mosquitto", 1883, 10) # service adı ile bağlantı
    client.connect("mosquitto", 1883, 60) # service adı ile bağlantı
    # client.connect("172.19.0.3", 1883, 60) # service adı ile bağlantı
    # client.connect("192.168.43.10", 1883, 60) # service adı ile bağlantı
    # client.connect("localhost", 1883, 60) # service adı ile bağlantı
    # client.connect("192.168.1.35", 1883, 60) # service adı ile bağlantı
    # client.connect("localhost", 1884, 60) # service adı ile bağlantı
    print("def run icinde client.connect gecti...")
    client.loop_start()
    # client.loop_forever # Döngüyü başlat (bloklamayan)
    print("def run icinde client.loop_forever gecti...")


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