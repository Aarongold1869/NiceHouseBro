from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username

class SavedProperty(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    property_id = models.CharField(max_length=100)
    
    class Meta:
        constraints = [
            models.UniqueConstraint('profile', 'property_id', name='profile-property_id'),
        ]
    
    def __str__(self):
        return f'{self.profile.user.username} - {str(self.property_id)}'
    

