from django.conf import settings
from django.shortcuts import render

from api.redfin import fetch_property_list_from_map_data
from api.redfin.redfin_types import Property

from typing import List

def home_view(request):
    # property_list: List[Property] = property_search_api(search_str='Pensacola, FL')
    property_list: List[Property] = []
    context = {
        'property_list': property_list, 
    }
    return render(request, 'home.html', context)

def faq_view(request, slug:str='', *args, **kwargs):
    faqs = [
        {
            'slug': 'about-us',
            'question': 'What is NiceHouseBro?',
            'answer': 'NiceHouseBro is a real estate investment platform that helps you find the best investment properties in your area.'
        },
        {
            'slug': 'get-started',
            'question': 'How do I get started?',
            'answer': 'To get started, simply create an account and start searching for properties in your area.'
        },
        {
            'slug': 'contact-support',
            'question': 'How do I contact support?',
            'answer': 'You can contact support by emailing ...'
        },
        {
            'slug': 'rental-estimate',
            'question': 'How is a property\'s rental estimate calculated?',
            'answer': 'A property\'s rental estimate is calculated based on the property\'s price, location, and other factors.'
        }
    ]
    return render(request, 'faq.html', {'faqs': faqs})