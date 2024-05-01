from django.contrib import admin

from .models import SavedProperty, Comment, CommentLike, Reply, ReplyLike

# Register your models here.
admin.site.register(SavedProperty)
admin.site.register(Comment)
admin.site.register(CommentLike)
admin.site.register(Reply)
admin.site.register(ReplyLike)