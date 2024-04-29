from django.contrib import admin

from .models import SavedProperty, Comment

# Register your models here.
admin.site.register(SavedProperty)
admin.site.register(Comment)