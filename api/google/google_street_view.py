from django.conf import settings
from django.core.files.base import ContentFile

import base64
from functools import lru_cache
import requests

@lru_cache
def google_street_view_api_base64(address:str) -> str:
    print('fetch image')
    params = {
        "key": settings.GOOGLE_MAPS_API_KEY,
        "location": address,
        "size": "1000x500"
    }
    res = requests.get('https://maps.googleapis.com/maps/api/streetview', params=params)
    if res.ok:
        uri = f"data:{res.headers['Content-Type']};base64,{base64.b64encode(res.content).decode('utf-8')}"
        res.close()
    else:
        uri = ''
    return uri
