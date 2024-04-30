from django.contrib import admin

from .models import SavedProperty, Comment, Reply

# Register your models here.
admin.site.register(SavedProperty)
admin.site.register(Comment)
admin.site.register(Reply)