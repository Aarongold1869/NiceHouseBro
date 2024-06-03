from django.db import models
from django.contrib.auth.models import User

# Create your models here.
GOAL_CHOICES = [
    ('Searching for Investment Property', 'Searching for Investment Property'),
    ('Searching for New Home', 'Searching for New Home'),
    ('Moving Soon', 'Moving Soon'),
    ('Just Browsing', 'Just Browsing'),
    ('Other', 'Other')
]

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    theme = models.CharField(choices=[('light','light'), ('dark','dark')], max_length=100, default='light')
    goal = models.CharField(choices=GOAL_CHOICES, max_length=100, default='Searching for Investment Property')
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    
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
    