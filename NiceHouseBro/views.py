from django.shortcuts import render

def home_view(request):
    # Your code here
    return render(request, 'home.html')
