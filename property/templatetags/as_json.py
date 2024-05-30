from django import template
import json

register = template.Library()

@register.filter(name='as_json')
def as_json(value)-> str:
    return json.dumps(value)