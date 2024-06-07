from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUser(AbstractUser):
    # You can add fields that you want in your form not included in the Abstract User here
    # e.g Gender = model.CharField(max_length=10)
    USER_TYPE_CHOICES = (
        ('buyer', 'Buyer'),
        ('agent', 'Agent'),
        # ('teamlead', 'Teamlead'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default=USER_TYPE_CHOICES[0])

    @property
    def profile(self):
        return self.profile_set.first()

    @property
    def is_agent(self):
        return self.user_type == 'agent'
    
    objects = BaseUserManager()