from django.contrib import admin

from .models import Comment, CommentLike, Reply, ReplyLike, ReportForm

# Register your models here.
admin.site.register(Comment)
admin.site.register(CommentLike)
admin.site.register(Reply)
admin.site.register(ReplyLike)
admin.site.register(ReportForm)