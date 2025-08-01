from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User

from django_htmx.http import trigger_client_event
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field

from .models import Profile, BlockedUser, CapRateFormula, GOAL_CHOICES
from .forms import UpdateProfileForm, CapRateForm
from property.functions import calculate_cap_rate
from property.models import SavedProperty
from api.redfin import property_detail_api

import ast
import json
import os

# Create your views here.
@login_required(login_url='/account/login/')
def profile_view(request, username:str, *args, **kwargs):
    profile = Profile.objects.get(user__username=username)
    # profile.user.refresh_from_db()
    form = UpdateProfileForm(initial={ 
        'first_name': profile.user.first_name, 
        'last_name': profile.user.last_name, 
        'email': profile.user.email, 
        'phone_number': profile.phone_number, 
        'location': profile.location, 
        'goal': ast.literal_eval(profile.goal)
    })
    return render(request, 'profile/profile-detail.html', {'profile': profile, 'form': form })

def validate_email(request):
    form = UpdateProfileForm(request.GET)
    return HttpResponse(as_crispy_field(form['email']))

import re
def validate_phone_number(request):
    form = UpdateProfileForm(request.GET)
    phone_number = request.GET.get('phone_number', None)
    pattern = re.compile("(0|91)?[6-9][0-9]{9}")
    if not pattern.match(phone_number):
        form.add_error('phone_number', 'Invalid phone number')
    # print(as_crispy_field(form['phone_number']))
    return HttpResponse(as_crispy_field(form['phone_number']))

@login_required(login_url='/account/login/')
@require_http_methods(['POST'])
def update_profile_view(request, profile_id:int, *args, **kwargs):
    user: User = request.user
    profile = Profile.objects.get(id=profile_id, user=user)
    form = UpdateProfileForm(request.POST)
    if not form.is_valid():
        return HttpResponse(status=500)
    
    user.first_name = form.cleaned_data.get('first_name')
    user.last_name = form.cleaned_data.get('last_name')
    user.email = form.cleaned_data.get('email')
    user.save()
    profile.phone_number = form.cleaned_data.get('phone_number')
    profile.location = form.cleaned_data.get('location')
    profile.goal = form.cleaned_data.get('goal')
    profile.save()
    return render(request, 'profile/profile-detail.html', {'profile': profile, 'form': form })
    
@login_required(login_url='/account/login/')
def saved_property_list_view(request, *args, **kwargs):
    profile = Profile.objects.get(user=request.user)
    saved_properties_qs = SavedProperty.objects.filter(profile=profile).filter(archived=False).order_by('-timestamp')
    return render(request, 'profile/saved-properties.html', { 'profile': profile, 'saved_properties': saved_properties_qs })

@login_required(login_url='/account/login/')
@require_http_methods(['POST'])
def toggle_property_saved_view(request, property_id: str, *args, **kwargs):
    profile = Profile.objects.get(user=request.user)
    saved_qs = SavedProperty.objects.filter(profile=profile, property_id=property_id)
    if not saved_qs.exists():
        return HttpResponse(status=400)
    saved_qs.first().delete()
    return render(request, 'profile/partials/property-removed.html')

@login_required(login_url='/account/login/')
@require_http_methods(['POST'])
def update_profile_picture(request, *args, **kwargs):
    profile = Profile.objects.get(user=request.user)
    file = request.FILES.get('file-input', None)
    if file:
        if profile.profile_picture:
            if os.path.exists(profile.profile_picture.path):
                os.remove(profile.profile_picture.path)
        profile.profile_picture = file
        profile.save()
    return render(request, 'profile/partials/profile-img.html', {'profile': profile })

@login_required(login_url='/account/login/')
@require_http_methods(['GET'])
def toggle_theme(request, *args, **kwargs):
    profile = Profile.objects.get(user=request.user)
    if profile.theme == 'light':
        profile.theme = 'dark'
    else:
        profile.theme = 'light'
    profile.save()
    return HttpResponse(status=200)

def locate_view(request, *args, **kwargs):
    response = HttpResponse(status=200)
    response.set_cookie('coordinates', json.dumps(request.GET))
    return response

@login_required(login_url='/account/login/')
@require_http_methods(['POST'])
def block_user_view(request, blocked_user_id:int ):
    if request.user.id == blocked_user_id:
        return HttpResponse(status=500)
    profile = Profile.objects.get(user=request.user)
    BlockedUser.objects.create(profile=profile, blocked_user=blocked_user_id)
    response = HttpResponse(status=200)
    return trigger_client_event(response, 'reload-comments')

# @login_required(login_url='/account/login/')
@require_http_methods(['GET'])
def retrieve_new_formula_table(request, *args, **kwargs):
    property_value = int(request.GET.get('property_value', 100000))
    rent = int(request.GET.get('rent', 1000))
    
    form = None
    formula_obj = CapRateFormula()
    form_state = request.GET.get('form_state', None) # either initial or reset
    if form_state:
        if form_state == 'initial' and request.user.is_authenticated:
            formula_obj, created = CapRateFormula.objects.get_or_create(profile=request.user.profile) 
        form = CapRateForm(instance=formula_obj)

    annual_gross_income, annual_operating_expenses, net_operating_income, cap_rate = calculate_cap_rate(
                            value=property_value, 
                            rent=rent,
                            annual_property_tax_rate=float(request.GET.get('annual_property_tax_rate', formula_obj.annual_property_tax_rate)), 
                            monthly_management_fee_rate=float(request.GET.get('monthly_management_fee_rate', formula_obj.monthly_management_fee_rate)), 
                            monthly_insurance=int(request.GET.get('monthly_insurance', formula_obj.monthly_insurance)), 
                            monthly_maintance_as_rate=float(request.GET.get('monthly_maintance_as_rate', formula_obj.monthly_maintance_as_rate)), 
                            monthly_leasing_fee=int(request.GET.get('monthly_leasing_fee', formula_obj.monthly_leasing_fee)), 
                            monthly_hoa_fee=int(request.GET.get('monthly_hoa_fee', formula_obj.monthly_hoa_fee)), 
                            monthly_utilities=int(request.GET.get('monthly_utilities', formula_obj.monthly_utilities))
                        )
    

    context = {
        'property_value': property_value,
        'rent': rent,
        'annual_gross_income': annual_gross_income,
        'annual_operating_expenses': annual_operating_expenses,
        'net_operating_income': net_operating_income,
        'cap_rate': cap_rate,
        'form': form
    }
    return render(request, 'components/partials/cap-rate-formula-table.html', context)

@login_required(login_url='/account/login/')
@require_http_methods(['POST'])
def update_cap_rate_formula(request, *args, **kwargs):
    formula, created = CapRateFormula.objects.get_or_create(profile=request.user.profile)
    form = CapRateForm(instance=formula, data=request.POST)
    if not form.is_valid():
        return HttpResponse(status=500)
    form.save()
    return render(request, 'components/partials/cap-rate-form-success.html', {})

