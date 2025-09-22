from django.contrib import admin
from .models import Temperature,Device,Alarm,Event,RFID_Kisi,RFID_Etiket

@admin.register(Temperature)
class TemperatureAdmin(admin.ModelAdmin):
    list_display=[
        'pk',
        'device_name',
        'temperature',
        'date',
        'mail',
        # 'giris00',
        # 'giris01',
        # 'giris02',
        # 'giris03',
        # 'cikis0',
        # 'cikis00',
        # 'cikis01',
        # 'cikis02',
        # 'cikis03',
        'tag_id',
        'staff_name',
    ]
@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display=[
        'pk',
        'device_name',
        'device_ip',
        'device_port',
        'device_function',
    ]
@admin.register(RFID_Kisi)
class DeviceAdmin(admin.ModelAdmin):
    list_display=[
        'pk',
        'tag_id',
        'staff_name',
    ]
@admin.register(RFID_Etiket)
class DeviceAdmin(admin.ModelAdmin):
    list_display=[
        'pk',
        'tag_id',
        'staff_name',
        'cikis3',
        'date',
    ]
@admin.register(Alarm)
class AlarmAdmin(admin.ModelAdmin):
    list_display=[
        'pk',
        'alarm_id',
        'alarm_name',
    ]
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display=[
        'pk',
        'device_id',
        'device_name',
        'alarm_id',
        'alarm_name',
        'start_time',
        'finish_time',
        'info',
    ]
