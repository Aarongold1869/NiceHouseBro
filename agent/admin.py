from django.contrib import admin
from .models import AgentProfile, Wallet, Lead, AgentContactForm

# Register your models here.
@admin.register(AgentContactForm)
class AgentContactFormAdmin(admin.ModelAdmin):
    list_display = ('lead_profile', 'address', 'name', 'email', 'phone_number', 'message', 'financing_info')

admin.site.register(AgentProfile)
admin.site.register(Lead)
admin.site.register(Wallet)