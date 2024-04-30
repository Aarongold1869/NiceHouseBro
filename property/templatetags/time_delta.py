from django import template

from datetime import datetime
import pytz
UTC = pytz.timezone('UTC')

register = template.Library()

@register.filter(name='time_delta')
def time_delta(value: datetime)-> str:
    now = datetime.now().astimezone(UTC)
    delta = now - value
    if delta.days > 365:
        return f'{delta.days // 365}y'
    elif delta.days > 30:
        return f'{delta.days // 30}m'
    elif delta.days > 1:
        return f'{delta.days}d'
    elif delta.seconds > 3600:
        return f'{delta.seconds // 3600}h'
    elif delta.seconds > 60:
        return f'{delta.seconds // 60}min'
    else:
        return f'{delta.seconds}s'