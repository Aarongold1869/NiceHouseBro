from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    theme = models.CharField(choices=[('light','light'), ('dark','dark')], max_length=100, default='dark')
    
    def __str__(self):
        return self.user.username

class BlockedUser(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    blocked_user = models.IntegerField()
    
    class Meta:
        constraints = [
            models.UniqueConstraint('profile', 'blocked_user', name='profile-blocked_user'),
        ]
    
    def __str__(self):
        return f'{self.profile.user.username} - {self.blocked_user}'