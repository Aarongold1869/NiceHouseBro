from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username

class SavedProperty(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    property_id = models.IntegerField()
    
    def __str__(self):
        return self.property_id
