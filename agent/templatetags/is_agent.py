from django import template
from django.contrib.auth.models import User

register = template.Library() 

@register.filter(name='is_agent') 
def is_agent(user: User, group_name='Agent'):
    return user.groups.filter(name=group_name).exists() 