from django import forms
from django.urls import reverse_lazy

from .models import AgentContactForm

class AgentRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=10)
    email = forms.EmailField()
    zip_code = forms.CharField(max_length=5)


class AgentContactFormForm(forms.ModelForm):
    class Meta:
        model = AgentContactForm
        fields = ['user', 'address', 'name', 'email', 'phone_number', 'message', 'financing_info']
        widgets = {
            'user': forms.HiddenInput(),
            'address': forms.HiddenInput(),
            'message': forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': 'I am interested in this property...'}),
            'phone_number': forms.TextInput(attrs={
                'hx-get': reverse_lazy('validate_phone_number'),
                'hx-trigger': 'keyup',
                'hx-target': '#div_id_phone_number',
            })
        }
        labels = {
            'financing_info': 'I am interested in financing options.'
        }