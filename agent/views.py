from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import QuerySet
from django.shortcuts import render

from .forms import AgentRegistrationForm
from .models import AgentProfile, Lead

from django_htmx.http import trigger_client_event

# Create your views here.
def is_agent(user: User)-> bool:
    return user.groups.filter(name='Agent').exists()

def agent_splash_view(request):
    return render(request, 'agent/agent-splash.html')

def agent_register_view(request):
    form = AgentRegistrationForm()
    return render(request, 'agent/agent-register.html', {'form': form})

def subscription_view(request):
    ...

@login_required(login_url='/login/')
@user_passes_test(is_agent, login_url='/agents/register/')
def purchase_credit_view(request):
    ...

@login_required(login_url='/login/')
@user_passes_test(is_agent, login_url='/agents/register/')
def agent_dashboard_view(request):
    return render(request, 'agent/dashboard.html')

@login_required(login_url='/login/')
@user_passes_test(is_agent, login_url='/agents/register/')
def agent_profile_view(request):
    ...

@login_required(login_url='/login/')
@user_passes_test(is_agent, login_url='/agents/register/')
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
@user_passes_test(is_agent, login_url='/agents/register/')
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
@user_passes_test(is_agent, login_url='/agents/register/')
def create_listing_view(request):
    ...


