from django import template

register = template.Library()

@register.filter(name='decimal')
def decimal(value: float|str)-> str:
    if type(value) == str:
        value = float(value)
    return f'{value*100:.0f}'