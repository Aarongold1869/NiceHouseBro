from django import template

register = template.Library()

@register.filter(name='currency')
def currency(value: float, decimal: int)-> str:
    return f'${value:,.{decimal}f}'