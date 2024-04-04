from django.conf import settings

import base64
from functools import cache
import requests

@cache
def google_street_view_api(address:str) -> str | None:
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
        uri = None
    return uri