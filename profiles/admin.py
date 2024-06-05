from django.contrib import admin

from .models import Profile, BlockedUser, UserSearches 

# Register your models here.
admin.site.register(Profile)
admin.site.register(UserSearches)
admin.site.register(BlockedUser)