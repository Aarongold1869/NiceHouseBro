from django.db import models
from profiles.models import Profile
from django.conf import settings

User = settings.AUTH_USER_MODEL

import random
# Create your models here.

class AgentProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=100)
    license_state = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint('user', name='unique-agent'),
        ]
 
class Wallet(models.Model):
    agent = models.ForeignKey(AgentProfile, on_delete=models.CASCADE)
    credits = models.IntegerField(default=0)

class Lead(models.Model):
    agent = models.ForeignKey(AgentProfile, on_delete=models.CASCADE)
    lead_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    lead_score = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint('agent', 'lead_profile', name='agent-lead'),
        ]

class AgentContactForm(models.Model):
    lead_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    assigned_agent = models.ForeignKey(AgentProfile, on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10)
    message = models.TextField()
    financing_info = models.BooleanField(default=False)