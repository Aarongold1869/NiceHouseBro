from django import forms

class AgentRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=10)
    email = forms.EmailField()
    zip_code = forms.CharField(max_length=5)