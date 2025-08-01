from django import template

register = template.Library()

@register.filter(name='percentage')
def percentage(value: float|str)-> str:
    if type(value) == str:
        value = float(value)
    return f'{value*100:.2f}%'