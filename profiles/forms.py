from django import forms 
from .models import GOAL_CHOICES

from django.urls import reverse_lazy

class UpdateProfileForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={
                'hx-get': reverse_lazy('validate_email'),
                'hx-trigger': 'change',
                'hx-target': '#div_id_email',
            }))
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=16, required=False, widget=forms.TextInput(attrs={
                'hx-get': reverse_lazy('validate_phone_number'),
                'hx-trigger': 'change',
                'hx-target': '#div_id_phone_number',
            }))
    location = forms.CharField(max_length=100, required=False)
    goal = forms.ChoiceField(choices=GOAL_CHOICES)
