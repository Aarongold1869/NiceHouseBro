from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import render, redirect 

from .forms import AgentRegistrationForm, AgentContactFormForm
from .models import AgentProfile, Lead
from account.models import CustomUser
from profiles.models import Profile



# Create your views here.
def is_agent(user: CustomUser) -> bool:
    return user.is_agent

def agent_splash_view(request):
    return render(request, 'agent/agent-splash.html')

def agent_register_view(request):
    user: CustomUser = request.user
    profile = Profile.objects.get(user=user)
    if user.is_agent:
        return redirect('/agent/dashboard/')
    initial_data = {}
    if user.is_authenticated:
        initial_data = {'first_name': user.first_name, 'last_name': user.last_name, 'phone_number': profile.phone_number, 'email': user.email, 'zip_code': ''}
    form = AgentRegistrationForm(initial=initial_data)
    if request.method == 'POST':
        print(request.POST)
        form = AgentRegistrationForm(request.POST)
        if form.is_valid():
            print('is valid')
            AgentProfile.objects.create(user=user, license_number='123', license_state='FL')
            user.user_type = 'agent'
            user.save()
            return redirect('/agent/dashboard/')
        else:
            print(form.errors)
    return render(request, 'agent/agent-register.html', {'form': form})

def subscription_view(request):
    ...

@login_required(login_url='/login/')
@user_passes_test(is_agent, login_url='/agent/register/')
def purchase_credit_view(request):
    ...

@login_required(login_url='/login/')
@user_passes_test(is_agent, login_url='/agent/register/')
def agent_dashboard_view(request):
    return render(request, 'agent/dashboard.html')

@login_required(login_url='/login/')
@user_passes_test(is_agent, login_url='/agent/register/')
def agent_profile_view(request):
    ...

@login_required(login_url='/login/')
@user_passes_test(is_agent, login_url='/agent/register/')
def lead_procurment_view(request):
    ...

def get_next_sort_order(sort_order: str) -> str:
    if sort_order == 'asc':
        sort_order_next = 'desc'
    elif sort_order == 'desc':
        sort_order_next = ''
    else:
        sort_order_next = 'asc'
    return sort_order_next

@login_required(login_url='/login/')
@user_passes_test(is_agent, login_url='/agent/register/')
def crm_view(request):
    agent = AgentProfile.objects.get(user=request.user)
    leads = Lead.objects.filter(agent=agent, archived=False)
    sort_field = ''
    sort_order = ''
    if request.htmx:
        sort_field = request.GET.get('sort_field')
        sort_order = request.GET.get('sort_order')
        if sort_field == 'lead_score':
            leads = sorted(leads, key=lambda l: l.lead_score, reverse=(sort_order == 'desc'))
        elif sort_field == 'first_name' or sort_field == 'last_name':
            leads = sorted(leads, key=lambda l: l.lead.__dict__[sort_field], reverse=(sort_order == 'desc'))

    context = {
        'leads': leads,
        'sort_field': sort_field,
        'sort_order': sort_order,
        'sort_order_next': get_next_sort_order(sort_order)
    }
    return render(request, 'agent/my-leads.html', context)

@login_required(login_url='/login/')
@user_passes_test(is_agent, login_url='/agent/register/')
def create_listing_view(request):
    ...

import re
@login_required(login_url='/login/')
def post_agent_contact_form_view(request):
    contact_form = AgentContactFormForm(request.POST or None)
    phone_number = request.POST.get('phone_number', None)
    pattern = re.compile("(0|91)?[6-9][0-9]{9}")
    if not pattern.match(phone_number):
        contact_form.add_error('phone_number', 'Invalid phone number')
    if not contact_form.is_valid():
        return render(request, 'property/partials/agent-contact-form.html', {'contact_form': contact_form})
    contact_form.save()
    return HttpResponse('<p>Form Submitted Successfully! <br>An agent should be in contact with you soon.</p>', status=200)
    