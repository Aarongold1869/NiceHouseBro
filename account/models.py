from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username

class SavedProperty(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    property_id = models.CharField(max_length=100)
    
    class Meta:
        constraints = [
            models.UniqueConstraint('account', 'property_id', name='account-property_id'),
        ]
    
    def __str__(self):
        return f'{self.account.user.username} - {str(self.property_id)}'
    

