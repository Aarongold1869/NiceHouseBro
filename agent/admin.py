from django.contrib import admin
from .models import AgentProfile, Wallet, Lead

# Register your models here.
admin.site.register(AgentProfile)
admin.site.register(Lead)
admin.site.register(Wallet)