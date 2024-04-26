from django.shortcuts import render

from .forms import AgentRegistrationForm

# Create your views here.

def agent_splash_view(request):
    return render(request, 'agent/agent-splash.html')

def agent_register_view(request):
    form = AgentRegistrationForm()
    return render(request, 'agent/agent-register.html', {'form': form})

def subscription_view(request):
    ...

def purchase_credit_view(request):
    ...

def agent_dashboard_view(request):
    ...

def agent_profile_view(request):
    ...

def lead_procurment_view(request):
    ...

def crm_view(request):
    ...

def create_listing_view(request):
    ...


