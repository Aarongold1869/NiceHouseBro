from django.contrib import admin

from .models import Profile, BlockedUser

# Register your models here.
admin.site.register(Profile)
admin.site.register(BlockedUser)