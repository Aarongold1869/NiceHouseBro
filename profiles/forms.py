from django import forms 

from .models import GOAL_CHOICES

class UpdateProfileForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=10)
    location = forms.CharField(max_length=100)
    goal = forms.CharField(max_length=100)