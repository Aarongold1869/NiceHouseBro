from functools import lru_cache
from geopy.geocoders import Nominatim

@lru_cache
def nominatim_boundry_api(search_str: str, reverse:bool=False)-> dict:
    app = Nominatim(user_agent="NHB")
    if not reverse:
        location = app.geocode(search_str, geometry='geojson', addressdetails=True)
    else:
        # app = GoogleV3(api_key=settings.GOOGLE_MAPS_API_KEY)
        res = app.reverse(search_str)
        if not res:
            return None
        location = app.geocode(res.raw['address'], geometry='geojson', addressdetails=True)
    return location
