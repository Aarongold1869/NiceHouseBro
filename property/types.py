from typing import TypedDict, List, Dict

class Coordinates(TypedDict):
    lat: float
    lng: float

class Address(TypedDict):
    address: str
    city: str
    county: str
    state: str
    street: str
    zip: int

class MapData(TypedDict):
    coordinates: Coordinates
    boundry: List[str]
    zoom: int
    bounding_box: List[str]
    address: Address

class Property(TypedDict):
    ### ReAPI ############################
    absenteeOwner: bool
    address: Address
    adjustableRate: bool
    airConditioningAvailable: bool
    assessedImprovementValue: int
    assessedLandValue: int
    assessedValue: int
    auction: bool
    basement: bool
    bathrooms: int
    bedrooms: int
    cashBuyer: bool
    corporateOwned: bool
    death: bool
    distressed: bool
    documentType: str
    documentTypeCode: str
    equity: bool
    equityPercent: int
    estimatedEquity: int
    estimatedValue: int
    floodZone: bool
    floodZoneDescription: str
    floodZoneType: str
    foreclosure: bool
    forSale: bool
    freeClear: bool
    garage: bool
    highEquity: bool
    id: str
    inherited: bool
    inStateAbsenteeOwner: bool
    investorBuyer: bool
    landUse: str
    lastMortgage1Amount: str
    lastSaleAmount: str
    lastSaleDate: str
    latitude: float
    lenderName: str
    listingAmount: str
    longitude: float
    lotSquareFeet: int
    mailAddress: Address
    medianIncome: str
    MFH2to4: bool
    MFH5plus: bool
    mlsActive: bool
    mlsCancelled: bool
    mlsDaysOnMarket: int
    mlsFailed: bool
    mlsHasPhotos: bool
    mlsLastSaleDate: str
    mlsLastStatusDate: str
    mlsListingDate: str
    mlsListingPrice: int
    mlsPending: bool
    mlsSold: bool
    mlsStatus: str
    mlsType: str
    negativeEquity: bool
    neighborhood: Dict
    openMortgageBalance: int
    outOfStateAbsenteeOwner: bool
    owner1FirstName: str
    owner1LastName: str
    owner2FirstName: str
    owner2LastName: str
    ownerOccupied: bool
    preForeclosure: bool
    privateLender: bool
    propertyId: str
    propertyType: str
    propertyUse: str
    propertyUseCode: int
    rentAmount: str
    reo: bool
    roomsCount: int
    squareFeet: int
    suggestedRent: str
    unitsCount: int
    vacant: bool
    yearBuilt: str
    yearsOwned: int
    
    image: str
    
    ###### Zillow zestimate API
    # id: str
    # city: str
    # state: str
    # address: str
    # postal_code: str
    # Laitude: float
    # Longitude: float
    # Coordinates: List[float]
    # zestimate: int
    # rental_zestimate: int
    # # other property details 
    # price: int 
    # bedrooms: int 
    # bathrooms: int 
    # area: int 
    # cap_rate: float 
    # cover_image_url: str 
    # image_array: List[str] 
    # is_saved: bool | None


class NominatimApiReponse(TypedDict):
    place_id: int
    licence: str
    osm_type: str
    osm_id: int
    lat: str
    lon: str
    class_: str
    type: str
    place_rank: int
    importance: float
    addresstype: str
    name: str
    display_name: str
    boundingbox: List[str]
    geojson: List[str]
    addressdetails: Address
