from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

from profiles.models import GOAL_CHOICES

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=10, required=False)

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "username", "email", "phone_number", "password1", "password2"]

class LocationForm(forms.Form):
    location = forms.CharField(max_length=100)

class GoalForm(forms.Form):
    realestate_goal = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=GOAL_CHOICES)