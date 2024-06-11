from django import forms 
from .models import GOAL_CHOICES, CapRateFormula

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
    goal =  forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=GOAL_CHOICES)


CAP_RATE_HTMX_ATTRS = {
    'hx-get': reverse_lazy('retrieve_new_formula'),
    'hx-trigger': 'change',
    'hx-target': '#cap-rate-formula-table',
    'hx-include': "[name='property_value'], [name='rent'], [name='annual_property_tax_rate'], [name='monthly_management_fee_rate'], [name='monthly_insurance'], [name='monthly_maintance_as_rate'], [name='monthly_leasing_fee'], [name='monthly_hoa_fee'], [name='monthly_utilities']"
}

class CapRateForm(forms.ModelForm):

    class Meta:
        model = CapRateFormula
        fields = '__all__'
        exclude = ['profile']
        labels = {
            'annual_property_tax_rate': 'Property Tax Rate (%)',
            'monthly_management_fee_rate': 'Management Fee Rate (%)',
            'monthly_insurance': 'Monthly Insurance ($)',
            'monthly_maintance_as_rate': 'Maintance Fee Rate (%)',
            'monthly_leasing_fee': 'Monthly Leasing Fee ($)',
            'monthly_hoa_fee': 'Monthly HOA Fee ($)',
            'monthly_utilities': 'Monthly Utilities ($)'
        }
        widgets = {
            'annual_property_tax_rate': forms.NumberInput(attrs={'step': 0.0001, 'min':0, **CAP_RATE_HTMX_ATTRS}),
            'monthly_management_fee_rate': forms.NumberInput(attrs={'step': 0.01, 'min':0, **CAP_RATE_HTMX_ATTRS}),
            'monthly_insurance': forms.NumberInput(attrs={'step': 1, 'min':0, **CAP_RATE_HTMX_ATTRS}),
            'monthly_maintance_as_rate': forms.NumberInput(attrs={'step': .01, 'min':0, **CAP_RATE_HTMX_ATTRS}),
            'monthly_leasing_fee': forms.NumberInput(attrs={'step': 1, 'min':0, **CAP_RATE_HTMX_ATTRS}),
            'monthly_hoa_fee': forms.NumberInput(attrs={'step': 1, 'min':0, **CAP_RATE_HTMX_ATTRS}),
            'monthly_utilities': forms.NumberInput(attrs={'step': 1, 'min':0, **CAP_RATE_HTMX_ATTRS})
        }