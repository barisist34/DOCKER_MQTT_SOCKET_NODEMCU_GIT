from apscheduler.schedulers.background import BackgroundScheduler,BlockingScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone
from django_apscheduler.models import DjangoJobExecution
from app_monitor.views import scheduler_cihaz
import sys
from app_monitor.views import Device,Event
from datetime import datetime

# This is the function you want to schedule - add as many as you want and then register them in the start() function below
def first_task_view():
    today = timezone.now()

    ...
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
        if device.event_set.filter(alarm_id=1).last() is None:# CİHAZ KESİK Mİ?
            if (datetime.timestamp(datetime_now) - datetime.timestamp(device.temperature_set.last().date) > 360):# and (device.event_set.last().event_active==False): #saha kesikse ve event en son aktif değilse(saha çalışıyorsa),yeni event ekle.
                device.device_state=False
                new_event=Event(device_id=device,device_name=device.device_name,alarm_id=1,alarm_name="Cihaz Kesik",start_time=datetime_now)
                new_event.save()
                print(f"(device.event_set.last().event_active):{device.event_set.last().event_active}")
        else:# CİHAZ KESİK Mİ?
            if (datetime.timestamp(datetime_now) - datetime.timestamp(device.temperature_set.last().date) > 360) and (device.event_set.last().event_active==False): #saha kesikse ve event en son aktif değilse(saha çalışıyorsa),yeni event ekle.
                device.device_state=False
                new_event=Event(device_id=device,device_name=device.device_name,alarm_id=1,alarm_name="Cihaz Kesik",start_time=datetime_now)
                new_event.save()
                print(f"(device.event_set.last().event_active):{device.event_set.last().event_active}")
        if device.event_set.filter(alarm_id=2).last() is None: # CIKIŞ_1 KESİK Mİ?
            # print(f"device.event_set.filter(alarm_id=2).last() is None: OK")
            print(f"ILK KAYIT device.temperature_set.last().cikis1: {device.temperature_set.last().cikis1}")
            print(f"ILK KAYIT device.temperature_set.last(): {device.temperature_set.last()}")
            print(f"ILK KAYIT device.temperature_set.last().cikis1: {type(device.temperature_set.last().cikis1)}")
            if (device.temperature_set.last().cikis1) == "LOW":# 
                print(f"device.temperature_set.last().cikis1==LOW: OK")
                new_event=Event(device_id=device,device_name=device.device_name,alarm_id=2,alarm_name="Çıkış-1 Down",start_time=datetime_now)
                new_event.save()
                print(f"Çıkış1 event:{device.event_set.last()}")
        else:
            print(f"KAYITLAR VAR device.temperature_set.last().cikis1: {device.temperature_set.last().cikis1}, length:{len(device.temperature_set.last().cikis1)} ")
            strip_test=device.temperature_set.last().cikis1.strip('"')
            print(f"STRIP KAYITLAR VAR device.temperature_set.last().cikis1: {strip_test}, length:{len(strip_test)} ")
            print(f"KAYITLAR VAR device.temperature_set.last(): {device.temperature_set.last()}")
            print(f"KAYITLAR VAR device.temperature_set.last().cikis1: {type(device.temperature_set.last().cikis1)}")   
            print(f"if (device.temperature_set.last().cikis1 is LOW ? : ): {(device.temperature_set.last().cikis1 is 'LOW')}")         
            print(f"STRIP if (device.temperature_set.last().cikis1 is LOW ? : ): {( strip_test == 'LOW')}")         
            if (device.temperature_set.last().cikis1.strip('"') == "LOW") and (device.event_set.last().event_active==False):
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
            print(f"event clear bloğuna girdi...event.device_id:{event.device_id}, event.id:{event.id}")
            device_state_now=True
            if event.event_active == True: #event devam ediyorsa
                event.event_active=False #event düzeldi yap
                event.finish_time=datetime.now()
                event.save()
            else:
                pass # event olarak devam etmiyorsa

    events_cihaz_kontrol=Event.objects.filter(alarm_id=2)
    print(f"events_cihaz_kontrol: {events_cihaz_kontrol.count()}")
    # print(f"events: {events}")
    #EVENT clear yapma:
    for event in events_cihaz_kontrol:
        # print(f"events_cihaz_kontrol,alarm ID: {event.alarm_id}")
    # for device in devices_all:
        if event.device_id.temperature_set.last().cikis1 == "HIGH": # cikis1 HIGH ise
            print(f"cikis1 clear bloğuna girdi...event.device_id:{event.device_id}, event.id:{event.id}")
            device_state_now=True
            if event.event_active == True: #event devam ediyorsa
                event.event_active=False #event düzeldi yap
                event.finish_time=datetime.now()
                event.save()
            else:
                pass # event olarak devam etmiyorsa


def start():
    scheduler = BackgroundScheduler() # 2 defa aynı job çalışıyor,yani düzensiz. start tan sonraki print server ilk başlayınca yazdırılıyor sadece. 
    # scheduler = BlockingScheduler() # normal çalışıyor,start sonrası print bloke ediliyor,hiç yazdırılmıyor. Server çalışmasını bloke ediyor,sadece kendi taskı çalışıyor.
    # scheduler.add_jobstore(DjangoJobStore(), "default") # bu komut olursa çoklu defa düzensiz çalışıyor.
    # run this job every 24 hours
    # scheduler.add_job(first_task_view, 'interval', hours=24, name='clean_accounts', jobstore='default')
    job=scheduler.add_job(first_task_view, 'interval', seconds=30, name='clean_accounts', jobstore='default')
    # job=scheduler.add_job(scheduler_cihaz, 'interval', seconds=30, name='clean_accounts', jobstore='default')
    # register_events(scheduler)
    scheduler.start()
    # job.remove()
    print("blocking yada backgroundscheduler kontrolu...")
    print("Scheduler started...", file=sys.stdout)