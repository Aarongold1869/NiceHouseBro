from django import forms 
from .models import GOAL_CHOICES

from django.urls import reverse_lazy

class UpdateProfileForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
                # 'hx-get': reverse_lazy('validate_email'),
                # 'hx-trigger': 'keyup',
                # 'hx-target': '#div_id_email',
            }))
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=10, required=False)
    location = forms.CharField(max_length=100, required=False)
    goal = forms.ChoiceField(choices=GOAL_CHOICES)
