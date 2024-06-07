from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from .forms import RegisterForm, LocationForm, GoalForm
from profiles.models import Profile

# Create your views here.

REGISTER_STEPS = {
    1: { "form": RegisterForm, 'title': 'Create an Account', 'button_text': 'Register', 'step': 1 },
    2: { "form": LocationForm, 'title': 'Where are you from?', 'button_text': 'Next', 'step': 2 },
    3: { "form": GoalForm, 'title': 'What are your realestate goals?', 'button_text': 'Finish', 'step': 3 }
}

def register_step_1_view(request, *args, **kwargs):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password1'))
            if user is not None:
                login(request, user)
                Profile.objects.create(user=user, phone_number=form.cleaned_data['phone_number'])
                return redirect("/account/register/step-2/")
    context = { "form": form, 'title': 'Create an Account', 'button_text': 'Register', 'step': 1 }
    return render(request, "account/register.html", context)

def register_step_2_view(request, *args, **kwargs):
    form = LocationForm()
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            profile = Profile.objects.get(user=request.user)
            profile.location = form.cleaned_data['location']
            profile.save()
            return redirect("/account/register/step-3/")
    context = { "form": form, 'title': 'Where are you from?', 'button_text': 'Next', 'step': 2, 'progress': f'Step 2 of {len(REGISTER_STEPS)}' }
    return render(request, "account/register.html", context)

def register_step_3_view(request, *args, **kwargs):
    form = GoalForm()
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            profile = Profile.objects.get(user=request.user)
            profile.goal = form.cleaned_data['realestate_goal']
            profile.save()
            return redirect("/")
    context = { "form": form, 'title': 'What are your realestate goals?', 'button_text': 'Finish', 'step': 3, 'progress': f'Step 3 of {len(REGISTER_STEPS)}' }
    return render(request, "account/register.html", context)

def login_view(request, *args, **kwargs):
    form = AuthenticationForm()
    form_error = None
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            form_error = 'Invalid Username or Password.'
    context = {
        'form_error': form_error,
        'form': form
    }
    return render(request, 'account/login.html', context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('/account/login/')

