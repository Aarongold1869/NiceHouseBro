from django import template

register = template.Library()

@register.filter(name='comma')
def comma(value: float)-> str:
    return f'{value:,.0f}'