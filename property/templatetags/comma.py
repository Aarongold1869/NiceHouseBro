from django import template

register = template.Library()

@register.filter(name='comma')
def comma(value: float)-> str:
    if type(value) == int:
        return f'{value:,.0f}'
    return value