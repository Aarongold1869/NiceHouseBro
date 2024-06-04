from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    header = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    link_href = models.CharField(max_length=255, null=True, blank=True)
    link_alt_text = models.CharField(max_length=255, null=True, blank=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['is_read', '-timestamp']

    def __str__(self):
        return f"{self.header} - {self.user.username}"
    
