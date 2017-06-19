"""template custom filters"""
import json
from django import template
from django.utils.safestring import mark_safe


register = template.Library()

@register.filter(name='split')
def split(value, arg):
    """template custom split filter"""
    return value.split(arg)

@register.filter(name='to_int')
def to_int(value):
    """template custom to int filter"""
    return int(value)

@register.filter(is_safe=True)
def to_js(obj):
    """template custom to json filter"""
    return mark_safe(json.dumps(obj))
