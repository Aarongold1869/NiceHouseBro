from typing import List, Dict, TypedDict

class ValueDict(TypedDict):
    value: str | int | Dict
    level: int

class Property(TypedDict):
    mlsId: str
    showMlsId: bool
    mlsStatus: str
    price: ValueDict
    hideSalePrice: bool
    hoa: ValueDict
    sqFt: ValueDict
    pricePerSqFt: ValueDict
    lotSize: ValueDict
    beds: int
    baths: float
    fullBaths: int
    location: ValueDict
    stories: float
    latLong: ValueDict
    streetLine: ValueDict
    unitNumber: ValueDict
    city: str
    state: str
    zip: str
    postalCode: ValueDict
    countryCode: str
    showAddressOnMap: bool
    soldDate: int
    searchStatus: int
    propertyType: int
    uiPropertyType: int
    listingType: int
    propertyId: int
    listingId: int
    dataSourceId: int
    marketId: int
    yearBuilt: ValueDict
    dom: ValueDict
    timeOnRedfin: ValueDict
    originalTimeOnRedfin: ValueDict
    timeZone: str
    primaryPhotoDisplayLevel: int
    photos: ValueDict
    alternatePhotosInfo: dict
    additionalPhotosInfo: List[dict]
    scanUrl: str
    posterFrameUrl: str
    listingBroker: dict
    sellingBroker: dict
    listingAgent: dict
    openHouseStart: int
    openHouseEnd: int
    openHouseStartFormatted: str
    openHouseEventName: str
    url: str
    hasInsight: bool
    sashes: List[dict]
    isHot: bool
    hasVirtualTour: bool
    hasVideoTour: bool
    has3DTour: bool
    newConstructionCommunityInfo: dict
    isRedfin: bool
    isNewConstruction: bool
    listingRemarks: str
    remarksAccessLevel: int
    servicePolicyId: int
    businessMarketId: int
    buildingId: int
    isShortlisted: bool
    isViewedListing: bool

class RedfinSearchPagePayload(TypedDict):
    homes: List[Property]
    dataSources: List[dict]
    buildings: dict
    searchMedian: dict
    serviceRegionName: str
    csvDownloadLinkDisplayLevel: int
    hasBrokerInformation: bool

class RedfinDetailPagePayload(TypedDict):
    ...

class RedfinResponse(TypedDict):
    version: int
    errorMessage: str
    resultCode: int
    payload: RedfinSearchPagePayload | RedfinDetailPagePayload

''' 
Redfin response data structure:

{}&amp;&amp; {
    "version":532,
    "errorMessage":"Success",
    "resultCode":0,
    "payload":{
        "homes":[{
            "mlsId":{
                "label":"MLS#",
                "value":"2225532"
                },
            "showMlsId":false,
            "mlsStatus":"Active",
            "showDatasourceLogo":true,
            "price":{
                "value":313500,
                "level":1
            },
            "hideSalePrice":false,
            "hoa":{
                "value":672,
                "level":1
            },
            "isHoaFrequencyKnown":true,
            "sqFt":{
                "value":980,
                "level":1
            },
            "pricePerSqFt":{
                "value":320,
                "level":1
            },
            "lotSize":{
                "level":1
            },
            "beds":2,
            "baths":2.0,
            "fullBaths":2,
            "location":{
                "value":"Seattle",
                "level":1
            },
            "stories":1.0,
            "latLong":{
                "value":{
                    "latitude":47.4998584,
                    "longitude":-122.3360967
                },
                "level":1
            },
            "streetLine":{
                "value":"138 SW 116th St Unit G12",
                "level":1
            },
            "unitNumber":{
                "value":"Unit G12",
                "level":1
            },
            "city":"Seattle",
            "state":"WA",
            "zip":"98146",
            "postalCode":{
                "value":"98146",
                "level":1
            },
            "countryCode":"US",
            "showAddressOnMap":true,
            "soldDate":1185778800000,
            "searchStatus":1,
            "propertyType":3,
            "uiPropertyType":2,
            "listingType":1,
            "propertyId":20738,
            "listingId":186586229,
            "dataSourceId":1,
            "marketId":1,
            "yearBuilt":{
                "value":1982,
                "level":1
            },
            "dom":{
                "value":1,
                "level":1
            },
            "timeOnRedfin":{
                "value":66537842,
                "level":1
            },
            "originalTimeOnRedfin":{
                "value":66537852,
                "level":1
            },
            "timeZone":"US/Pacific",
            "primaryPhotoDisplayLevel":1,
            "photos":{
                "value":"0-29:0",
                "level":1
            },
            "alternatePhotosInfo":{
                "mediaListType":"1",
                "mediaListIndex":0,
                "groupCode":"894971_JPG",
                "positionSpec":[38,46,37,40,41,21,27,22,26,29,32,30,33,35,14,19,16,17,15,13,20,6,7,8,10,12,4,45,47,2],
                "type":1
            },
            "additionalPhotosInfo":[],
            "scanUrl":"https://my.matterport.com/show/?m\u003dteaueD3tFGF",
            "posterFrameUrl":"https://my.matterport.com/api/v2/player/models/teaueD3tFGF/thumb",
            "listingBroker":{
                "name":"Redfin",
                "isRedfin":true
            },
            "sellingBroker":{
                "isRedfin":false
            },
            "listingAgent":{
                "name":"Shelle Dier",
                "redfinAgentId":34495
            },
            "openHouseStart":1713646800000,
            "openHouseEnd":1713654000000,
            "openHouseStartFormatted":"Apr 20,2:00PM",
            "openHouseEventName":"Open House - 2:00 - 4:00 PM",
            "url":"/WA/Seattle/138-SW-116th-St-98146/unit-G12/home/20738",
            "hasInsight":true,
            "sashes":[
                {
                "sashType":10,
                "sashTypeId":10,
                "sashTypeName":"Open House",
                "sashTypeColor":"#73BB3C",
                "isRedfin":true,
                "openHouseText":"OPEN SAT,2PM TO 4PM",
                "lastSaleDate":"",
                "lastSalePrice":""
                },
                {
                "sashType":31,
                "sashTypeId":31,
                "sashTypeName":"3D Walkthrough",
                "sashTypeColor":"#7556F2",
                "isRedfin":false,
                "openHouseText":"",
                "lastSaleDate":"",
                "lastSalePrice":""
                }
            ],
            "isHot":false,
            "hasVirtualTour":true,
            "hasVideoTour":false,
            "has3DTour":true,
            "newConstructionCommunityInfo":{},
            "isRedfin":true,
            "isNewConstruction":false,
            "listingRemarks":"SELLER WILL PAY 1-year of HOAs with a full price offer (up to $8064)  \u0026amp;  PRICE IMPROVEMENT! Ground level unit with private backyard area off of the patio; tranquil territorial views. This two bedroom,two bath home lives large! Oversized bedrooms are on opposite sides of the unit for privacy,\u0026amp;  each has access to a bathroom. Full-size laundry in unit. Storage closet off of patio. All hard surface flooring. Dedicated carport parking space with many visitor spots. HOAs include water/sewer,cable, garbage and common areas. Newer appliances. Convenient access to SeaTac Airport, 509, 518, I5, and 405. Shop in Burien or nearby Westwood Village. Nearby bus lines. Home Inspection and all H",
            "remarksAccessLevel":1,
            "servicePolicyId":14,
            "businessMarketId":1,
            "buildingId":64770,
            "isShortlisted":false,
            "isViewedListing":false
        }
        ],
        "dataSources":[{
            "id":1,
            "name":"NWMLS as Distributed by MLS Grid",
            "description":"Northwest Multiple Listing Service (NWMLS)",
            "disclaimer":"\u003cimg src\u003d\"${IMAGE_SERVER}/images/logos/nwmls_small.png\" /\u003e\u003cp\u003eBased on information submitted to the MLS GRID as of ${CURRENT_DATE}. All data is obtained from various sources and may not have been verified by broker or MLS GRID. Supplied Open House Information is subject to change without notice. All information should be independently reviewed and verified for accuracy. Properties may or may not be listed by the office/agent presenting the information. Some IDX listings have been excluded from this website.\u003c/p\u003e",
            "logo":"nwmls_small.png",
            "canShowInFooter":false,
            "homecardTextAttribution":true
        }],
        "buildings":{
            "64770":{
                "id":64770,
                "address":{
                    "streetNumber":"138",
                    "directionalPrefix":"SW",
                    "streetName":"116th",
                    "streetType":"St",
                    "directionalSuffix":"",
                    "unitType":"",
                    "unitValue":"",
                    "city":"Seattle",
                    "stateOrProvinceCode":"WA",
                    "postalCode":"98146",
                    "countryCode":"US"
                },
            "buildingName":"138 SW 116th St, Seattle, WA 98146",
            "numUnitsForSale":1,
            "url":"/WA/Seattle/138-SW-116th-St-Seattle-WA-98146/building/64770",
            "responseCode":200
            }
        },
        "searchMedian":{
            "price":313500,
            "sqFt":980,
            "pricePerSqFt":320,
            "dom":1,
            "beds":2,
            "baths":2.0
        },
        "serviceRegionName":"white-center-south-park",
        "csvDownloadLinkDisplayLevel":3,
        "hasBrokerInformation":true 
    }
}
    
'''