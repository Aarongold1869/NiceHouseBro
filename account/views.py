from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import RegisterForm
import json

# Create your views here.

# Create your views here.
def register_view(request, *args, **kwargs):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password1'))
            if user is not None:
                login(request, user)
                return redirect("/")
        else:
            return render(request, "account/register.html", {"form":form})
    else:
        form = RegisterForm()
        return render(request, "account/register.html", {"form":form})


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
    return redirect('/accounts/login/')

def locate_view(request, *args, **kwargs):
    response = HttpResponse(status=200)
    response.set_cookie('coordinates', json.dumps(request.GET))
    return response