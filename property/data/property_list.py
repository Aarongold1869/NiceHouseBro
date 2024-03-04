from typing import TypedDict, List

class Property(TypedDict):
    address: str
    price: int
    bedrooms: int
    bathrooms: int
    area: int
    cap_rate: float
    image_url: str

PROPERTY_DATA: List[Property] = [
    {
        "id": 1,
        "address": "123 Main St",
        "price": 100000,
        "bedrooms": 3,
        "bathrooms": 2,
        "area": 1500,
        "cap_rate": 0.1,
        "cover_image_url": "media/awesome-house.jpg",
        "image_array": ["media/awesome-house.jpg", "media/hoarder-house.jpg", "media/shrek.webp"]
    },
    {
        "id": 2,
        "address": "456 Gregory St",
        "price": 275000,
        "bedrooms": 2,
        "bathrooms": 2,
        "area": 2000,
        "cap_rate": 0.4,
        "cover_image_url": "media/awesome-house.jpg",
        "image_array": ["media/awesome-house.jpg", "media/hoarder-house.jpg", "media/shrek.webp"]
    },
    {
        "id": 3,
        "address": "789 Alcaniz St",
        "price": 320000,
        "bedrooms": 4,
        "bathrooms": 3,
        "area": 2500,
        "cap_rate": 0.35,
        "cover_image_url": "media/awesome-house.jpg",
        "image_array": ["media/awesome-house.jpg", "media/hoarder-house.jpg", "media/shrek.webp"]
    },
    {
        "id": 4,
        "address": "1011 Garden St",
        "price": 152000,
        "bedrooms": 3,
        "bathrooms": 2,
        "area": 1700,
        "cap_rate": 0.1,
        "cover_image_url": "media/awesome-house.jpg",
        "image_array": ["media/awesome-house.jpg", "media/hoarder-house.jpg", "media/shrek.webp"]
    },
    {
        "id": 5,
        "address": "1213 Taragona St",
        "price": 75000,
        "bedrooms": 1,
        "bathrooms": 1,
        "area": 900,
        "cap_rate": 0.08,
        "cover_image_url": "media/awesome-house.jpg",
        "image_array": ["media/awesome-house.jpg", "media/hoarder-house.jpg", "media/shrek.webp"]
    },
]
