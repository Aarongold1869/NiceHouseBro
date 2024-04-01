from django.contrib import admin

from .models import Profile, SavedProperty

# Register your models here.
admin.site.register(Profile)
admin.site.register(SavedProperty)