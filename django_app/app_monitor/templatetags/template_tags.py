from django import template
from app_monitor.models import Device
from datetime import datetime

register = template.Library()  ## CUSTOM TEMPLATE FILTER BUILD

@register.filter # register the template filter with django
def subtract_dates(value): # Only one argument.
    """Evaluate a string if it contains []"""
    """Evaluate a string if it contains []"""
    if '[' and ']' in value:
        return eval(value)
@register.filter
def subtract_datetime(date1,date2):
    duration=date1-date2
    # print(f"type_duration_tags: {type(duration)}, date1: {type(date1)}")
    return str(duration).split(".")[0]

@register.filter
def subtract_now_datetime(date):
    duration=datetime.now() - date
    # print(f"type_duration_tags: {type(duration)}, date1: {type(date)}")
    return str(duration).split(".")[0]
# <td>{{devices.temperature_set.first.date|add:"devices.temperature_set.first.date"}} </td>  

@register.filter
def last_event_active(devices,alarm_id):
    try:
        last_event=devices.event_set.filter(alarm_id=alarm_id).last()
        last_event_status=last_event.event_active
        if last_event_status == True:
            print("last_event_active: TRUE")
            return True
        else:
            print("last_event_active: FALSE")
            return False
    except Exception as e:
        print(f"EXCEPTION: last_event_active; {str(e)} ")
        return "-"

@register.filter
def last_event_startdate(devices,alarm_id):
    try:
        last_event=devices.event_set.filter(alarm_id=alarm_id).last()
        last_event_startdate_formatsiz=last_event.start_time
        # tarih2_formatli=datetime.strftime(tarih2_datetime,'%Y-%m-%d %H:%M') #datetime format değiştirme
        last_event_startdate=datetime.strftime(last_event_startdate_formatsiz,'%d-%m-%Y / %H:%M:%S')
        return last_event_startdate
    except Exception as e:
        print(f"EXCEPTION: last_event_startdate; {str(e)} ")
        return "-"

@register.filter
def last_event_finishdate(devices,alarm_id):
    try:
        last_event=devices.event_set.filter(alarm_id=alarm_id).last()
        print(f"devices.event_set.filter(alarm_id=alarm_id).last(): {devices.event_set.filter(alarm_id=alarm_id).last()}")
        last_event_finishtdate_formatsiz=last_event.finish_time
        print(f"last_event.finish_time: {last_event.finish_time}")
        last_event_finishdate=datetime.strftime(last_event_finishtdate_formatsiz,'%d-%m-%Y / %H:%M:%S')
        print("datetime.strftime(last_event_finishtdate_formatsiz,'%d-%m-%Y %H:%M:%S'): {last_event_finishdate}")
        return last_event_finishdate
    except Exception as e:
        print(f"EXCEPTION: last_event_finishdate; {str(e)} ")
        return "-"

@register.filter
def last_event_duration(devices,alarm_id):
    try:
        last_event=devices.event_set.filter(alarm_id=alarm_id).last()
        last_event_duration=last_event.event_duration
        last_event_startdate_formatsiz=last_event.start_time
        # tarih2_formatli=datetime.strftime(tarih2_datetime,'%Y-%m-%d %H:%M') #datetime format değiştirme
        last_event_startdate=datetime.strftime(last_event_startdate_formatsiz,'%d-%m-%Y %H:%M')
        return last_event_startdate
    except Exception as e:
        print(f"EXCEPTION: last_event_duration; {str(e)} ")
        return "-"

@register.filter
def active_device_duration(devices,alarm_id):
    try:
        last_event=devices.event_set.filter(alarm_id=alarm_id).last()
        print(f"devices.event_set.filter(alarm_id=alarm_id).last(): {devices.event_set.filter(alarm_id=alarm_id).last()}")
        active_device_duration_formatsiz=datetime.now() - last_event.finish_time
        print(f"datetime.now() - last_event.finish_time: {datetime.now() - last_event.finish_time}")
        last_event_startdate_formatsiz=last_event.start_time
        # tarih2_formatli=datetime.strftime(tarih2_datetime,'%Y-%m-%d %H:%M') #datetime format değiştirme
        # active_device_duration=datetime.strftime(active_device_duration_formatsiz,'%Y-%m-%d %H:%M')
        # return active_device_duration_formatsiz
        return str(active_device_duration_formatsiz).split(".")[0]
    except Exception as e:
        print(f"EXCEPTION: active_device_duration; {str(e)} ")
        return "-"

@register.filter
def outage_device_duration(devices,alarm_id):
    try:
        last_event=devices.event_set.filter(alarm_id=alarm_id).last()
        print(f"devices.event_set.filter(alarm_id=alarm_id).last(): {devices.event_set.filter(alarm_id=alarm_id).last()}")
        outage_device_duration_formatsiz=datetime.now() - last_event.start_time
        print(f"datetime.now() - last_event.finish_time: {datetime.now() - last_event.start_time}")
        last_event_startdate_formatsiz=last_event.start_time
        # tarih2_formatli=datetime.strftime(tarih2_datetime,'%Y-%m-%d %H:%M') #datetime format değiştirme
        # active_device_duration=datetime.strftime(active_device_duration_formatsiz,'%Y-%m-%d %H:%M')
        # return outage_device_duration_formatsiz
        return str(outage_device_duration_formatsiz).split(".")[0]
    except Exception as e:
        print(f"EXCEPTION: active_device_duration; {str(e)} ")
        return "-"

# @register.filter
# def Takimlar_filter(queryset,filter):
#     return Takimlar.objects.filter(takim_adi=filter)
# register.filter('Takimlar_filter',Takimlar_filter)

# {% for j in takimlar|Takimlar_filter:puanlar.takim_adi %}

