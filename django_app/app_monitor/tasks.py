from background_task import background
from django.contrib.auth.models import User
from datetime import datetime

from django.utils import timezone
from app_monitor.views import scheduler_cihaz
import sys
from app_monitor.views import Device,Event,Temperature,RFID_Kisi
from datetime import datetime

@background(schedule=20)
def notify_user(user_id):
    # lookup user by id and send them a message
    user = User.objects.get(pk=user_id)
    user.email_user('Here is a notification', 'You have been notified')
    time=datetime.now()
    print(f"notify_user 20 saniyede tekrarlıyor...: {time}")

@background(schedule=20)
def notify_task_1(user_id):
    user = User.objects.get(pk=user_id)
    time=datetime.now()
    print(f"notify_task_1, 20 saniyede tekrarlıyor: {time} ")


# This is the function you want to schedule - add as many as you want and then register them in the start() function below

@background(schedule=20)
def first_task_view(user_id):
    today = timezone.now()

    ...
    print("******************************************************************")
    print(f"first_task_view başladı,20 saniyede bir tekrarlar: {today}")
    # scheduler_cihaz(request)
    # get accounts, expire them, etc.
    ...
   #event create yapılmalı,daha önce cihazın ilgili durumuyla ilgili event yoksa
    #aşağıda aktif eventler düzelip düzelmedikleri kontrol edilmelidir.
    #EVENT oluşturma:    
    datetime_now=datetime.now()

    devices_all=Device.objects.all()
    for device in devices_all:
        if device.temperature_set.last() is None:
            print(f"ilk temperature kayıt, device_id için")
            newRecord = Temperature(temperature=10,humidity=10 ,volcum=10,device_name=device.device_name,device_id=device, date=timezone.now(),cikis1=0,cikis2=0,tag_id=RFID_Kisi.objects.get(id=1),staff_name="add_first") #241013
            newRecord.save() # cihazda daha önce Temperature kaydı yoksa,prototip bir kayıt oluşturulur,sonraki if bloklarında hata oluşmaması için 
        # if device.event_set.filter(alarm_id=1).last() is None:# CİHAZ KESİK Mİ? (DATABASE GIRILDIGINDE VE CIHAZ HIC BAGLANMADIGINDA)
        if device.event_set.filter(alarm_id=1).last() is None and device.temperature_set.last() is not None:# CİHAZ KESİK Mİ? (İLK KESINTI EVENT KAYDI) (DATABASE GIRILDIGINDE VE CIHAZ HIC BAGLANMADIGINDA)
            # if (datetime.timestamp(datetime_now) - datetime.timestamp(device.temperature_set.last().date) > 360):# and (device.event_set.last().event_active==False): #saha kesikse ve event en son aktif değilse(saha çalışıyorsa),yeni event ekle.
            # if (datetime.timestamp(datetime_now) - datetime.timestamp(device.temperature_set.last().date) > 40):# and (device.event_set.last().event_active==False): #saha kesikse ve event en son aktif değilse(saha çalışıyorsa),yeni event ekle.
            device.device_state=False
            new_event=Event(device_id=device,device_name=device.device_name,alarm_id=1,alarm_name="Cihaz Kesik",start_time=datetime_now,event_active=False)
            new_event.save()
            print(f"(device.event_set.last().event_active):{device.event_set.last().event_active}")
            # Cihaz ilk Temp kaydını oluşturduğunda, beklemeden clear olarak prototip bir Event oluşturulur.
        # else:# CİHAZ KESİK Mİ?
        elif device.temperature_set.last() is not None:# CİHAZ KESİK Mİ?
            if (datetime.timestamp(datetime_now) - datetime.timestamp(device.temperature_set.last().date) > 330) and (device.event_set.last().event_active==False): #saha kesikse ve event en son aktif değilse(saha çalışıyorsa),yeni event ekle.
                device.device_state=False
                new_event=Event(device_id=device,device_name=device.device_name,alarm_id=1,alarm_name="Cihaz Kesik",start_time=datetime_now)
                new_event.save()
                print(f"(device.event_set.last().event_active):{device.event_set.last().event_active}")
        if device.event_set.filter(alarm_id=2).last() is None and device.temperature_set.last() is not None: # CIKIŞ_1 KESİK Mİ?
            # print(f"device.event_set.filter(alarm_id=2).last() is None: OK")
            # print(f"ILK KAYIT device.temperature_set.last().cikis1: {device.temperature_set.last().cikis1}")
            print(f"ILK KAYIT device.temperature_set.last(): {device.temperature_set.last()}")
            # print(f"device.event_set.filter(alarm_id=2).last(): {device.event_set.filter(alarm_id=2).last()}")
            # print(f"ILK KAYIT device.temperature_set.last().cikis1 type: {type(device.temperature_set.last().cikis1)}")
            # if (device.temperature_set.last().cikis1) == "LOW":# 
            if (device.temperature_set.last().cikis1) == "0":# 
                print(f"device.temperature_set.last().cikis1==LOW: OK")
                new_event=Event(device_id=device,device_name=device.device_name,alarm_id=2,alarm_name="Çıkış-1 Down",start_time=datetime_now)
                new_event.save()
                print(f"Çıkış1 event:{device.event_set.last()}")
        else:
            print(f"KAYITLAR VAR device.temperature_set.last().cikis1: {device.temperature_set.last().cikis1}, length:{len(device.temperature_set.last().cikis1)} ")
            strip_test=device.temperature_set.last().cikis1.strip('"')
            # print(f"STRIP KAYITLAR VAR device.temperature_set.last().cikis1: {strip_test}, length:{len(strip_test)} ")
            # print(f"KAYITLAR VAR device.temperature_set.last(): {device.temperature_set.last()}")
            # print(f"KAYITLAR VAR device.temperature_set.last().cikis1: {type(device.temperature_set.last().cikis1)}")   
            # print(f"if (device.temperature_set.last().cikis1 is LOW ? : ): {(device.temperature_set.last().cikis1 is 'LOW')}")         
            # print(f"STRIP if (device.temperature_set.last().cikis1 is LOW ? : ): {( strip_test == 'LOW')}")         
            # if (device.temperature_set.last().cikis1.strip('"') == "LOW") and (device.event_set.last().event_active==False):
            if (device.temperature_set.last().cikis1.strip('"') == "0") and (device.event_set.last().event_active==False):
                print(f"Çıkış1 event:{device.event_set.last()}")
                new_event=Event(device_id=device,device_name=device.device_name,alarm_id=2,alarm_name="Çıkış-1 Down",start_time=datetime_now)
                new_event.save()
                print(f"Çıkış1 event:{device.event_set.last()}")

    events_cihaz_kontrol=Event.objects.filter(alarm_id=1)
    print(f"events_cihaz_kontrol: {events_cihaz_kontrol.count()}")
    # print(f"events: {events}")
    #EVENT clear yapma:
    for event in events_cihaz_kontrol:
        # print(f"events_cihaz_kontrol,alarm ID: {event.alarm_id}")
    # for device in devices_all:
        if datetime.timestamp(datetime_now) - datetime.timestamp(event.device_id.temperature_set.last().date) < 360: #gerçekte online ise
            # print(f"event clear bloğuna girdi...event.device_id:{event.device_id}, event.id:{event.id}")
            device_state_now=True
            if event.event_active == True: #event devam ediyorsa
                event.event_active=False #event düzeldi yap
                event.finish_time=datetime.now()
                event.save()
            else:
                pass # event olarak devam etmiyorsa

    events_cihaz_kontrol_2=Event.objects.filter(alarm_id=2)
    print(f"events_cihaz_kontrol: {events_cihaz_kontrol_2.count()}")
    # print(f"events: {events}")
    #EVENT clear yapma:
    for event in events_cihaz_kontrol_2:
        # print(f"events_cihaz_kontrol,alarm ID: {event.alarm_id}")
    # for device in devices_all:
        # if event.device_id.temperature_set.last().cikis1 == "HIGH": # cikis1 HIGH ise
        if event.device_id.temperature_set.last().cikis1 == "1": # cikis1 HIGH ise
            print(f"cikis1 clear bloğuna girdi...event.device_id:{event.device_id}, event.id:{event.id}, event.event_active:{event.event_active}")
            device_state_now=True
            if event.event_active == True: #event devam ediyorsa
                print(f"event.event_active==True if bloguna girdi...")
                event.event_active=False #event düzeldi yap
                event.finish_time=datetime.now()
                event.save()
            else:
                pass # event olarak devam etmiyorsa
    print(f"first_task_view sonu: {datetime.now()} ")
    print("*"*30)