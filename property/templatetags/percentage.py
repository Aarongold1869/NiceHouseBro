from django import template

register = template.Library()

@register.filter(name='percentage')
def percentage(value: float)-> str:
    return f'{value*100:.2f}%'