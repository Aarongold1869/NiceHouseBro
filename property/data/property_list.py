from typing import TypedDict, List


# {
#     success: true,
#     status: 200,
#     bundle: [
#         {
#             id: "a855f55246b5ab4c4cd073f87684fdb9",
#             city: "Lubbock",
#             zpid: "252177367",
#             state: "TX",
#             address: "11213 Granby Ave Lubbock TX 79424-1441",
#             minus30: 319500,
#             Latitude: 33.490943,
#             Longitude: -101.944221,
#             timestamp: "2021-08-02T07:00:00.000Z",
#             zestimate: 322800,
#             zillowUrl: "https://www.zillow.com/homes/252177367_zpid/",
#             lowPercent: 9,
#             postalCode: "79424",
#             streetName: "Granby",
#             unitNumber: null,
#             unitPrefix: null,
#             highPercent: 10,
#             houseNumber: "11213",
#             zipPlusFour: "1441",
#             streetSuffix: "Ave",
#             directionPrefix: null,
#             directionSuffix: null,
#             rentalTimestamp: "2021-07-27T07:00:00.000Z",
#             rentalZestimate: 2105,
#             rentalLowPercent: 32,
#             rentalHighPercent: 22,
#             houseNumberFraction: null,
#             BridgeModificationTimestamp: "2021-08-03T17:20:48.415Z",
#             Coordinates: [
#                 -101.944221,
#                 33.490943
#             ],
#             forecastStandardDeviation: null,
#             url: "rets.io/api/v2/zestimates_v2/zestimates/a855f55246b5ab4c4cd073f87684fdb9"
#         }
#     ],
#     total: 1
# } 

# zillow api response
class Property(TypedDict):
    # Zillow zestimate API
    id: str
    city: str
    state: str
    address: str
    postal_code: str
    Laitude: float
    Longitude: float
    Coordinates: List[float]
    zestimate: int
    rental_zestimate: int
    # other property details 
    price: int 
    bedrooms: int 
    bathrooms: int 
    area: int 
    cap_rate: float 
    cover_image_url: str 
    image_array: List[str] 
    is_saved: bool | None

PROPERTY_DATA: List[Property] = [
    {
        "id": '1',
        "city": "Pensacola",
        "state": "FL",
        "address": "1987 Wyatt Street, Pensacola, FL 32504",
        "postal_code": "32504",
        "Laitude": 30.534720,
        "Longitude": -87.213210,
        "Coordinates": [30.534720, -87.213210],
        "zestimate": 100000,
        "rental_zestimate": 900,

        "price": 100000,
        "bedrooms": 3,
        "bathrooms": 2,
        "area": 1500,
        "cap_rate": 0.1,
        "cover_image_url": "media/awesome-house.jpg",
        "image_array": ["media/awesome-house.jpg", "media/hoarder-house.jpg", "media/shrek.webp"]
    },
    {
        "id": '2',
        "city": "Pensacola",
        "state": "FL",
        "address": "4810 Yacht Harbor Dr., Pensacola, FL 32514",
        "postal_code": "32514",
        "Laitude": 30.514750,
        "Longitude": -87.172610,
        "Coordinates": [30.514750, -87.172610],
        "zestimate": 275000,
        "rental_zestimate": 1400,
        
        "price": 275000,
        "bedrooms": 2,
        "bathrooms": 2,
        "area": 2000,
        "cap_rate": 0.4,
        "cover_image_url": "media/awesome-house.jpg",
        "image_array": ["media/awesome-house.jpg", "media/hoarder-house.jpg", "media/shrek.webp"]
    },
    {
        "id": '3',
        "city": "Milton",
        "state": "FL",
        "address": "5813 Guinevere Lane, Milton, FL 32583",
        "postal_code": "32583",
        "Laitude": 30.573601,
        "Longitude": -87.094902,
        "Coordinates": [30.573601, -87.094902],
        "zestimate": 320000,
        "rental_zestimate": 1400,
        
        "price": 320000,
        "bedrooms": 4,
        "bathrooms": 3,
        "area": 2500,
        "cap_rate": 0.35,
        "cover_image_url": "media/awesome-house.jpg",
        "image_array": ["media/awesome-house.jpg", "media/hoarder-house.jpg", "media/shrek.webp"]
    },
    {
        "id": '4',
        "city": "Virginia Beach",
        "state": "VA",
        "address": "1136 Las Cruces Dr., Virginia Beach, VA 23454",
        "postal_code": "23454",
        "Laitude": 36.772140,
        "Longitude": -76.008120,
        "Coordinates": [36.772140, -76.008120],
        "zestimate": 574000,
        "rental_zestimate": 2500,
    
        "price": 574000,
        "bedrooms": 3,
        "bathrooms": 2,
        "area": 1700,
        "cap_rate": 0.1,
        "cover_image_url": "media/awesome-house.jpg",
        "image_array": ["media/awesome-house.jpg", "media/hoarder-house.jpg", "media/shrek.webp"]
    },
    {
        "id": '5',
        "city": "Hermosa Beach",
        "state": "CA",
        "address": "616 24th St, Hermosa Beach, CA 90254",
        "postal_code": "90254",
        "Laitude": 33.870704,
        "Longitude": -118.3969845,
        "Coordinates": [33.870704, -118.3969845],
        "zestimate": 3413100,
        "rental_zestimate": 4000,
        
        "price": 3413100,
        "bedrooms": 1,
        "bathrooms": 1,
        "area": 900,
        "cap_rate": 0.08,
        "cover_image_url": "media/awesome-house.jpg",
        "image_array": ["media/awesome-house.jpg", "media/hoarder-house.jpg", "media/shrek.webp"]
    },
]
