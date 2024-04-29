from django.db import models
from profiles.models import Profile

# Create your models here.
class SavedProperty(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    property_id = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    image = models.CharField(max_length=99999, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    
    class Meta:
        constraints = [
            models.UniqueConstraint('profile', 'property_id', name='profile-property_id'),
        ]
    
    def __str__(self):
        return f'{self.profile.user.username} - {str(self.property_id)} - {self.timestamp}'
    
class Comment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    property_id = models.CharField(max_length=100)
    comment = models.CharField(max_length=999)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.profile.user.username} - {str(self.property_id)} - {self.timestamp}'