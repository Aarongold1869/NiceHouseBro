from django import template

register = template.Library()

@register.filter(name='remove_slashes')
def remove_slashes(value: str)-> str:
    return value.replace('/', '|')