from django import template

from datetime import datetime
import pytz
UTC = pytz.timezone('UTC')

register = template.Library()

@register.filter(name='time_delta')
def time_delta(value: datetime)-> str:
    now = datetime.now().astimezone(UTC)
    delta = now - value
    if delta.seconds < 60:
        return f'{delta.seconds}s'
    elif 60 <= delta.seconds < 3600:
        return f'{delta.seconds // 60}min'
    elif delta.days == 0:
        return f'{delta.min // 60}h'
    elif 1 <= delta.days < 30:
        return f'{delta.days}d'
    elif 30 <= delta.days < 365:
        return f'{delta.days // 30}m'
    else:
        return f'{delta.days // 365}y'