from django import template

register = template.Library()

@register.filter(name='currency')
def currency(value: str, decimal: int)-> str:
    if type(value) == str:
        if value == '':
            value = 0
        else:
            value = float(value)
    return f'${value:,.{decimal}f}'