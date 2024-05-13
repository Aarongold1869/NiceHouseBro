from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

from .forms import AgentRegistrationForm

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
    ...

@login_required(login_url='/login/')
@user_passes_test(is_agent, login_url='/agents/register/')
def agent_profile_view(request):
    ...

@login_required(login_url='/login/')
@user_passes_test(is_agent, login_url='/agents/register/')
def lead_procurment_view(request):
    ...

@login_required(login_url='/login/')
@user_passes_test(is_agent, login_url='/agents/register/')
def crm_view(request):
    ...

@login_required(login_url='/login/')
@user_passes_test(is_agent, login_url='/agents/register/')
def create_listing_view(request):
    ...


