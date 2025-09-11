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

# @register.filter
# def Takimlar_filter(queryset,filter):
#     return Takimlar.objects.filter(takim_adi=filter)
# register.filter('Takimlar_filter',Takimlar_filter)

# {% for j in takimlar|Takimlar_filter:puanlar.takim_adi %}