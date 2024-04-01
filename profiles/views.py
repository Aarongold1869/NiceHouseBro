from django.http import HttpResponse
from django.shortcuts import render

import json

# Create your views here.
def locate_view(request, *args, **kwargs):
    response = HttpResponse(status=200)
    response.set_cookie('coordinates', json.dumps(request.GET))
    return response