from django.db import models
from django.contrib.auth.models import User
from profiles.models import Profile
import re

# Create your models here.
class Comment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    property_id = models.CharField(max_length=100)
    property_address = models.CharField(max_length=250)
    property_url = models.CharField(max_length=1000)
    text = models.CharField(max_length=999)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.profile.user.username} - {str(self.property_id)} - {self.timestamp}'
    
    @property
    def comment_link(self):
        return f'/property/detail/{self.property_url}/#comment-{self.id}'

    @property
    def page_link(self):
        return f'#comment-{self.id}'
    
    
class CommentLike(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint('profile', 'comment', name='profile-comment'),
        ]
    
    def __str__(self):
        return f'{self.profile.user.username} - {str(self.comment.id)} - {self.timestamp}'
    

class Reply(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    text = models.CharField(max_length=999)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.profile.user.username} - {str(self.comment.id)} - {self.timestamp}'
    
    
class ReplyLike(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint('profile', 'reply', name='profile-reply'),
        ]

    def __str__(self):
        return f'{self.profile.user.username} - {str(self.reply.id)} - {self.timestamp}'
    
class ReportForm(models.Model):
    model = models.CharField(choices=[('Comment', 'Comment'), ('Reply', 'Reply')], max_length=10)
    object_id = models.IntegerField()
    reported_text = models.CharField(max_length=999)
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)
    timestamp = models.DateTimeField(auto_now_add=True)
    cause = models.CharField(choices=[
            ('Spam', 'Spam'), 
            ('Harrassment', 'Harrassment'), 
            ('Threatening Violence', 'Threatening Violence'), 
            ('Hate Speech', 'Hate Speech'), 
            ('Impersonation', 'Impersonation'),
            ('Prohibited Transaction', 'Prohibited Transaction'),
            ('Other', 'Other')
        ], 
        max_length=40)
    resolved = models.BooleanField(default=False)
    action = models.CharField(choices=[
            ('Delete', 'Delete'), 
            ('Ignore', 'Ignore'), 
            ('TempCommentBan', 'TempCommentBan'),
            ('CommentBan', 'CommentBan')
        ], 
        max_length=20, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)