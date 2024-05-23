from django.contrib import admin

from .models import Comment, CommentLike, Reply, ReplyLike, ReportForm

# Register your models here.

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('profile', 'property_id', 'property_address', 'text', 'timestamp', 'updated', 'archived')

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('profile', 'comment', 'text', 'timestamp', 'updated', 'archived')

admin.site.register(CommentLike)
admin.site.register(ReplyLike)
admin.site.register(ReportForm)