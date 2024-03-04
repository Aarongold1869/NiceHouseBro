from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

# Create your views here.

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
    return redirect('/')