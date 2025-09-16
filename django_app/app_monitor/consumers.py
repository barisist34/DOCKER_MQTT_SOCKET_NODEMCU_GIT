# chat/consumers.py
import json
from .models import Temperature,Device,Event,Alarm
from .views import event_list_view
from django.shortcuts import render, HttpResponse,redirect
from django.utils import timezone
import datetime
from asgiref.sync import async_to_sync
# from datetime import datetime

from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         print(f"self.scope: {self.scope}, type: {type(self.scope)} ")
#         print(f"CONNECTION self.scope['client']: {self.scope['client']} ")
#         print(f"CONNECTION self.scope['user']: {self.scope['user']} ")
#         print(f"CONNECTION self.scope['query_string']: {self.scope['query_string']} ")
#         # self.room_name = self.scope['path']
#         self.room_name = self.scope['client']
#         # self.room_group_name = f'chat_{self.room_name}'
#         self.room_group_name = f'chat_baris'

#         # Gruba katıl
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )

#         self.accept()
#         alarm_kesinti_object=Alarm.objects.get(alarm_id=1)
#         device_id_scope=int(self.scope['query_string'])
#         device_id_socket=Device.objects.get(device_id=device_id_scope)

#         # newRecord = Temperature(temperature=11,humidity= 33,volcum=12, date=timezone.now(),device_name="test",device_id=device_id_socket) #250610
#         # newRecord.save()
#         # print(f"newRecord: {newRecord}")
#         event_all_clear=Event.objects.filter(event_active=True,device_id=device_id_socket,alarm_id=alarm_kesinti_object) # clear olmayan aynı alarm id li hatalı eventlar varsa hepsini clear yapar.
#         for event in event_all_clear: 
#             event.event_active=False
#             event.finish_time=datetime.datetime.now()
#             event.save()
#         self.accept()


def chat_message(self, event):
# Gruptan gelen mesajı client'a gönder
    message = event['message']
    self.send(text_data=json.dumps({
    'message': message
    }))

# class ChatConsumer(WebsocketConsumer):
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(f"self.scope: {self.scope}, type: {type(self.scope)} ")
        print(f"CONNECTION self.scope['client']: {self.scope['client']} ")
        print(f"CONNECTION self.scope['user']: {self.scope['user']} ")
        print(f"CONNECTION self.scope['query_string']: {self.scope['query_string']} ")
        device_id_scope=int(self.scope['query_string'])
        # self.group_name = 'esp_group'
        self.group_name = f"esp_group_{device_id_scope}"
        print(f"self.group_name: {self.group_name}")
        print("commit yapabilmek için eklendi")
        #commit için

        # Gruba ekle
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

        # self.room_name = self.scope['path']
        #####self.room_name = self.scope['client']
        # self.room_group_name = f'chat_{self.room_name}'
        #####self.room_group_name = f'chat_baris'
        #####await self.accept()

        alarm_kesinti_object=await sync_to_async(Alarm.objects.get)(alarm_id=1)
        device_id_scope=int(self.scope['query_string'])
        device_id_socket=await sync_to_async(Device.objects.get)(device_id=device_id_scope)

        # newRecord = await sync_to_async(Temperature)(temperature=11,humidity= 33,volcum=12, date=timezone.now(),device_name=device_id_socket.device_name.capitalize(),device_id=device_id_socket) #250610
        # await sync_to_async(newRecord.save)()
        # print(f"newRecord: {newRecord}")
        event_all_clear=await sync_to_async(Event.objects.filter)(event_active=True,device_id=device_id_socket,alarm_id=alarm_kesinti_object) # clear olmayan aynı alarm id li hatalı eventlar varsa hepsini clear yapar.
        event_all_clear=await sync_to_async(list)(Event.objects.filter(event_active=True,device_id=device_id_socket,alarm_id=alarm_kesinti_object)) # clear olmayan aynı alarm id li hatalı eventlar varsa hepsini clear yapar.
        for event in event_all_clear: 
            event.event_active=False
            event.finish_time=datetime.datetime.now()
            await sync_to_async(event.save)()



    # def disconnect(self, close_code):
    async def disconnect(self, close_code):
        # Gruptan çıkar (DICONNECT OLUNCA GERI CONNECT OLMUYORDU, DISABLE ILE TEST OLACAK)
        # await self.channel_layer.group_discard(
        #     self.group_name,
        #     self.channel_name
        # )
        device_id_scope=int(self.scope['query_string'])
        device_id_socket=await sync_to_async(Device.objects.get)(device_id=device_id_scope)
        alarm_kesinti_object=await sync_to_async(Alarm.objects.get)(alarm_id=1)
        close_code=close_code

        print(f"DEVICE ID: {device_id_scope} kesildi...:{datetime.datetime.now()}")
        print(f"socket_disconnect girdi...   close code:{close_code}")
        print(f"DISCONNECT self.scope['client']: {self.scope['client']} ")
        new_input_event=await sync_to_async(Event)(device_id=device_id_socket,device_name=device_id_socket.device_name,alarm_id=alarm_kesinti_object,start_time=timezone.now(),event_active=True)
        await sync_to_async(new_input_event.save)()

    async def group_message(self, event):
        message = event['message']

        # Bu client’a mesajı gönder
        await self.send(text_data=json.dumps({
            'message': message
        }))

    # def receive(self, text_data):
    async def receive(self, text_data):
        # Gruptaki tüm clientlara mesajı gönder
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'group_message',
                # 'message': message
                'message': text_data
            }
        )
        print("consumer receive girdi...")

        # data = text_data.readline().decode('utf_8')
        # data = int(text_data)
        data = text_data
        print(f"consumer gelen_veri: {data}, type: {type(data)}")
        # text_data_json = json.loads(text_data)
        # message = text_data_json["message"]
        # device_id_socket=Device.objects.get(device_id=1)
        json_socket=json.loads(text_data)
        print(f"json_socket: {json_socket},type :{type(json_socket)}, ")
        # json_socket_sid=json_socket["sid"]
        if "CONNECTION" in text_data: # cihaz ilk bağlanınca gelir (ayrıca cihaz bağlantı sayfası refresh yapılınca self.group_name = 'esp_group' vasıtasıyla )
            alarm_kesinti_object=await sync_to_async(Alarm.objects.get)(alarm_id=1)
            device_id_scope=int(self.scope['query_string'])
            device_id_socket=await sync_to_async(Device.objects.get)(device_id=device_id_scope)   

            event_all_clear=await sync_to_async(list)(Event.objects.filter(event_active=True,device_id=device_id_socket,alarm_id=alarm_kesinti_object)) # clear olmayan aynı alarm id li hatalı eventlar varsa hepsini clear yapar.
            for event in event_all_clear: 
                event.event_active=False
                event.finish_time=datetime.datetime.now()
                await sync_to_async(event.save)()
                            
        if "sid" in text_data:
            json_socket_sid=int(json_socket['sid'])
            print(f"json_socket['sid']: {json_socket_sid},type :{type(json_socket_sid)} ")
            # device_id_socket=Device.objects.get(device_id=json_socket["sid"])
            device_id_socket=await sync_to_async(Device.objects.get)(device_id=json_socket["sid"])
            device_name_socket=json_socket["sname"]
            temperature_socket=json_socket["stemp"]
            humidity_socket=json_socket["shum"]
            volt_socket=json_socket["svolt"]
            # device_id_socket=Device.objects.get(device_id=1)
            # newRecord = Temperature(temperature=16,humidity=44 ,volcum=11, date=timezone.now(),device_name="Test",device_id=device_id_socket) #250610
            # newRecord = Temperature(temperature=16,humidity=44 ,volcum=11, date=timezone.now(),device_name=device_name_socket,device_id=device_id_socket) #250610
            newRecord = await sync_to_async(Temperature)(temperature=temperature_socket,humidity= humidity_socket,volcum=volt_socket, date=timezone.now(),device_name=device_name_socket,device_id=device_id_socket) #250610
            await sync_to_async(newRecord.save)()
            print(f"newRecord: {newRecord}")
            # self.send(text_data=json.dumps({"message": message}))
            # self.send(text_data=json.dumps({"message": str(timezone.now())}))
            # self.send(text_data=json.dumps({"message": str(timezone.localtime())}))
            self.send(text_data=json.dumps({"message": f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ve deger:{text_data} '}))
        if "INPUTLAR" in text_data:
            """
            json_socket_sid=int(json_socket['sid'])
            print(f"json_socket['sid']: {json_socket_sid},type :{type(json_socket_sid)} ")
            device_id_socket=Device.objects.get(device_id=json_socket["sid"])
            device_name_socket=json_socket["sname"]
            device_id_socket=Device.objects.get(device_id=json_socket["sid"])
            device_name_socket=json_socket["sname"]
            alarm_input1_object=Alarm.objects.get(alarm_id=8)
            json_socket_xi01=int(json_socket['si01'])
            print(f"si01: {json_socket_xi01} ")
            self.send(text_data=json.dumps({"message": f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ve deger:{text_data} '}))
            new_input_event=Event(device_id=device_id_socket,device_name=device_id_socket.device_name,alarm_id=alarm_input1_object,alarm_name="Giriş--01 Aktif",start_time=timezone.now(),event_active=True)
            new_input_event.save()
            """
            ### INPUT EVENT OLUŞTURMA

            # input0=request.GET.get("input0")
            # input1=request.GET.get("input1")
            # input0=int(json_socket['si00'])
            # input1=int(json_socket['si01'])
            input0=str(json_socket['si00'])
            print(f"input0:{input0}, type(input0):{type(input0)}")
            input1=str(json_socket['si01'])
            print(f"input1:{input1}, type(input1):{type(input1)}")
            input2=str(json_socket['si02'])
            print(f"input2:{input2}, type(input2):{type(input2)}")
            input3=str(json_socket['si03'])
            print(f"input3:{input3}, type(input3):{type(input3)}")
            input_no=str(json_socket['sinput_id'])
            print(f"input_no:{input_no}, type(input_no):{type(input_no)}")
            # input2=int(json_socket['si02'])
            # input3=int(json_socket['si03'])
            # input2=request.GET.get("input2")
            # input3=request.GET.get("input3")
            # etiket=request.GET.get("etiket") #250117
            json_socket_sid=int(json_socket['sid'])
            device_id_socket=await sync_to_async(Device.objects.get)(device_id=json_socket_sid)
            # device_id=request.GET.get("device_id") #250513
            device=await sync_to_async(Device.objects.get)(device_id=json_socket_sid) #250615
            datetime_now=datetime.datetime.now() #250513
            alarm_kesinti_object=await sync_to_async(Alarm.objects.get)(alarm_id=1)
            alarm_input0_object=await sync_to_async(Alarm.objects.get)(alarm_id=7)
            # print(f"input0_active_event_available: {input0_active_event_available}")
            alarm_input0_object=await sync_to_async(Alarm.objects.get)(alarm_id=7)
            input0_active_event_available=await sync_to_async(Event.objects.filter(alarm_id=alarm_input0_object).filter(event_active=True).filter(device_id=device).count)()
            alarm_input1_object=await sync_to_async(Alarm.objects.get)(alarm_id=8)
            input1_active_event_available=await sync_to_async(Event.objects.filter(alarm_id=alarm_input1_object).filter(event_active=True).filter(device_id=device).count)()
            print(f"input1:{input1}")
            print(f"input1_active_event_available:{input1_active_event_available}")
            alarm_input2_object=await sync_to_async(Alarm.objects.get)(alarm_id=9)
            input2_active_event_available=await sync_to_async(Event.objects.filter(alarm_id=alarm_input2_object).filter(event_active=True).filter(device_id=device).count)()
            alarm_input2_object=await sync_to_async(Alarm.objects.get)(alarm_id=9)
            alarm_input3_object=await sync_to_async(Alarm.objects.get)(alarm_id=10)
            input3_active_event_available=await sync_to_async(Event.objects.filter(alarm_id=alarm_input3_object).filter(event_active=True).filter(device_id=device).count)()
            if input0 or input1 or input2 or input3 == "1":
                if input_no=="0" and  input0 == "1" and input0_active_event_available == 0:
                    new_input_event=Event(device_id=device,device_name=device.device_name,alarm_id=alarm_input0_object,alarm_name="Giriş--00 Aktif",start_time=datetime_now,event_active=True)
                    new_input_event.save()
                    print(f"new_input_event--1: f{new_input_event}")
                    # event_list_view()
                    # return redirect('/app_monitor/event_list_view') 
                    redirect('/app_monitor/scheduler_cihaz')
                    print("redirect scheduler altı...")
                if input_no=="1" and  input1 == "1" and input1_active_event_available == 0:
                    new_input_event=await sync_to_async(Event)(device_id=device,device_name=device.device_name,alarm_id=alarm_input1_object,alarm_name="Giriş--01 Aktif",start_time=datetime_now,event_active=True)
                    await sync_to_async(new_input_event.save)()
                    print(f"new_input_event--1: f{new_input_event}")
                    redirect('/app_monitor/scheduler_cihaz')
                    print("redirect scheduler altı...")
                if input_no=="2" and  input2 == "1" and input1_active_event_available == 0:
                    new_input_event=await sync_to_async(Event)(device_id=device,device_name=device.device_name,alarm_id=alarm_input2_object,alarm_name="Giriş--02 Aktif",start_time=datetime_now,event_active=True)
                    await sync_to_async(new_input_event.save)()
                    print(f"new_input_event--1: f{new_input_event}")
                    redirect('/app_monitor/scheduler_cihaz')
                    print("redirect scheduler altı...")
                if input_no=="3" and input3 == "1" and input3_active_event_available == 0:
                    new_input_event=await sync_to_async(Event)(device_id=device,device_name=device.device_name,alarm_id=alarm_input3_object,alarm_name="Giriş--03 Aktif",start_time=datetime_now,event_active=True)
                    await sync_to_async(new_input_event.save)()
                    print(f"new_input_event--1: f{new_input_event}")
                    redirect('/app_monitor/scheduler_cihaz')
                    print("redirect scheduler altı...")
            if input_no=="0" and input0 == "0" and input0_active_event_available != 0: # alarm devam etmiyor ve aktif event varsa (count sayar)
                print(f"input0 == 0 and input0_active_event_available !=0 girdi...")
                event_all_clear=await sync_to_async(Event.objects.filter)(event_active=True,alarm_id=alarm_input0_object,device_id=device) # clear olmayan aynı alarm id li hatalı eventlar varsa hepsini clear yapar.
                for event in event_all_clear: 
                    event.event_active=False
                    event.finish_time=datetime.datetime.now()
                    event.save()
                print("event clear RETURN event_list_view////")
                # return redirect('/app_monitor/scheduler_cihaz')
                redirect('/app_monitor/scheduler_cihaz')
                print("redirect scheduler altı...clear")
            if input_no=="1" and input1 == "0" and input1_active_event_available != 0: # alarm devam etmiyor ve aktif event varsa (count sayar)
                print(f"input1 == 0 and input1_active_event_available !=0 girdi...")
                event_all_clear=await sync_to_async(list)(Event.objects.filter(event_active=True,alarm_id=alarm_input1_object,device_id=device)) # clear olmayan aynı alarm id li hatalı eventlar varsa hepsini clear yapar.
                for event in event_all_clear: 
                    event.event_active=False
                    event.finish_time=datetime.datetime.now()
                    # await sync_to_async(event.save)()
                    await sync_to_async(event.save)()
                print("event clear RETURN event_list_view////")
                # return redirect('/app_monitor/scheduler_cihaz')
                redirect('/app_monitor/scheduler_cihaz')
                print("redirect scheduler altı...clear")
            if input_no=="2" and input2 == "0" and input2_active_event_available != 0: # alarm devam etmiyor ve aktif event varsa (count sayar)
                print(f"input2 == 0 and input2_active_event_available !=0 girdi...")
                event_all_clear=await sync_to_async(list)(Event.objects.filter)(event_active=True,alarm_id=alarm_input2_object,device_id=device) # clear olmayan aynı alarm id li hatalı eventlar varsa hepsini clear yapar.
                for event in event_all_clear: 
                    event.event_active=False
                    event.finish_time=datetime.datetime.now()
                    event.save()
                print("event clear RETURN event_list_view////")
                # return redirect('/app_monitor/scheduler_cihaz')
                redirect('/app_monitor/scheduler_cihaz')
                print("redirect scheduler altı...clear")
            if input_no=="3" and input3 == "0" and input3_active_event_available != 0: # alarm devam etmiyor ve aktif event varsa (count sayar)
                print(f"input3 == 0 and input3_active_event_available !=0 girdi...")
                event_all_clear=await sync_to_async(list)(Event.objects.filter)(event_active=True,alarm_id=alarm_input3_object,device_id=device) # clear olmayan aynı alarm id li hatalı eventlar varsa hepsini clear yapar.
                for event in event_all_clear: 
                    event.event_active=False
                    event.finish_time=datetime.datetime.now()
                    event.save()
                print("event clear RETURN event_list_view////")
                # return redirect('/app_monitor/scheduler_cihaz')
                redirect('/app_monitor/scheduler_cihaz')
                print("redirect scheduler altı...clear")
    # def close(self, code=None, reason=None):
    async def close(self, code=None, reason=None):
        """
        Closes the WebSocket from the server end
        """
        message = {"type": "websocket.close"}
        print("socket_close girdi...")
        if code is not None and code is not True:
            message["code"] = code
        if reason:
            message["reason"] = reason
        super().send(message)