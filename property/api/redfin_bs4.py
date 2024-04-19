from bs4 import BeautifulSoup
import json
import requests
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

def scrape_redfin(url:str)-> List[Property]:
    headers={  
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", 
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,lt;q=0.8,et;q=0.7,de;q=0.6",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        pretty = soup.prettify().replace('{}&amp;&amp;', '')
        data = json.loads(pretty)["payload"]["homes"]
        return data
    else:
        print(response.status_code)
        print('Failed to scrape the URL')
        return []
    
def get_endpoint_from_args():
    gis = 'true'
    include_nearby_homes = 'true'
    market = 'seattle'
    num_homes = 1
    ord = 'redfin-recommended-asc'
    page_number = 2
    poly = '-122.54472%2047.44109%2C-122.11144%2047.44109%2C-122.11144%2047.78363%2C-122.54472%2047.78363%2C-122.54472%2047.44109'
    sf = '1,2,3,5,6,7'
    start = 0
    status = 1
    uipt = '1,2,3,4,5,6,7,8'
    endpoint = f'gis?al=1&include_nearby_homes={include_nearby_homes}&market={market}&num_homes={num_homes}&ord={ord}&page_number={page_number}&poly={poly}&sf={sf}&start={start}&status={status}&uipt={uipt}'
    # endpoint = 'gis?al=1&include_nearby_homes=true&market=seattle&num_homes=350&ord=redfin-recommended-asc&page_number=1&poly=-122.54472%2047.44109%2C-122.11144%2047.44109%2C-122.11144%2047.78363%2C-122.54472%2047.78363%2C-122.54472%2047.44109&sf=1,2,3,5,6,7&start=0&status=1&uipt=1,2,3,4,5,6,7,8&user_poly=-122.278298%2047.739783%2C-122.278985%2047.739783%2C-122.279671%2047.739783%2C-122.325677%2047.743015%2C-122.330483%2047.743015%2C-122.335290%2047.743015%2C-122.346276%2047.742554%2C-122.351769%2047.742092%2C-122.357262%2047.741168%2C-122.362756%2047.740245%2C-122.368249%2047.739321%2C-122.373742%2047.737936%2C-122.378548%2047.736551%2C-122.383355%2047.735165%2C-122.388161%2047.733780%2C-122.392968%2047.732856%2C-122.397088%2047.731471%2C-122.401208%2047.730085%2C-122.404641%2047.728238%2C-122.407388%2047.726390%2C-122.410134%2047.724081%2C-122.412194%2047.721771%2C-122.414254%2047.718999%2C-122.416314%2047.716228%2C-122.418374%2047.712532%2C-122.421120%2047.708835%2C-122.423867%2047.704677%2C-122.426614%2047.700056%2C-122.429360%2047.695434%2C-122.432107%2047.690813%2C-122.434853%2047.686190%2C-122.437600%2047.681568%2C-122.439660%2047.676945%2C-122.441033%2047.671859%2C-122.442406%2047.666310%2C-122.444466%2047.660298%2C-122.446526%2047.653823%2C-122.447900%2047.646885%2C-122.449960%2047.639946%2C-122.451333%2047.632543%2C-122.452020%2047.625139%2C-122.452020%2047.619122%2C-122.452020%2047.613105%2C-122.452020%2047.607087%2C-122.452020%2047.601994%2C-122.452020%2047.596438%2C-122.451333%2047.590881%2C-122.449960%2047.586250%2C-122.448586%2047.581619%2C-122.447213%2047.576987%2C-122.445153%2047.572818%2C-122.443093%2047.568648%2C-122.441033%2047.564942%2C-122.438973%2047.561235%2C-122.436227%2047.557992%2C-122.433480%2047.554748%2C-122.430734%2047.551967%2C-122.428674%2047.549187%2C-122.426614%2047.546869%2C-122.423867%2047.544552%2C-122.421120%2047.541771%2C-122.418374%2047.539453%2C-122.415627%2047.537136%2C-122.412881%2047.534818%2C-122.410134%2047.532500%2C-122.406014%2047.530182%2C-122.401894%2047.527864%2C-122.397775%2047.525545%2C-122.392968%2047.523691%2C-122.388161%2047.521372%2C-122.383355%2047.519517%2C-122.378548%2047.517662%2C-122.373055%2047.515807%2C-122.368249%2047.513952%2C-122.362756%2047.512561%2C-122.357262%2047.511170%2C-122.351769%2047.509314%2C-122.345589%2047.507923%2C-122.339410%2047.506995%2C-122.332543%2047.506068%2C-122.325677%2047.505140%2C-122.318810%2047.504212%2C-122.312630%2047.503285%2C-122.307137%2047.502821%2C-122.302331%2047.502357%2C-122.298211%2047.502357%2C-122.294091%2047.502357%2C-122.289285%2047.502821%2C-122.285165%2047.503748%2C-122.281045%2047.504676%2C-122.276925%2047.505604%2C-122.272805%2047.506532%2C-122.267999%2047.507923%2C-122.263192%2047.508851%2C-122.258385%2047.509314%2C-122.253579%2047.509778%2C-122.248772%2047.510242%2C-122.245339%2047.510242%2C-122.240533%2047.510706%2C-122.237099%2047.511170%2C-122.233666%2047.511633%2C-122.231606%2047.512561%2C-122.229546%2047.513025%2C-122.228173%2047.513952%2C-122.226800%2047.515344%2C-122.226113%2047.517199%2C-122.225426%2047.519517%2C-122.224053%2047.522299%2C-122.222680%2047.526009%2C-122.221993%2047.529718%2C-122.220620%2047.533427%2C-122.219247%2047.537136%2C-122.218560%2047.540844%2C-122.217187%2047.545016%2C-122.216500%2047.549650%2C-122.215127%2047.554748%2C-122.213067%2047.561235%2C-122.212380%2047.568648%2C-122.211694%2047.576524%2C-122.211694%2047.584861%2C-122.211694%2047.593660%2C-122.211694%2047.602920%2C-122.211694%2047.611716%2C-122.211694%2047.620048%2C-122.211694%2047.627452%2C-122.211694%2047.634856%2C-122.211694%2047.641796%2C-122.212380%2047.648735%2C-122.213754%2047.655211%2C-122.215127%2047.661223%2C-122.216500%2047.667235%2C-122.218560%2047.673246%2C-122.220620%2047.679256%2C-122.223367%2047.684341%2C-122.226113%2047.688964%2C-122.228173%2047.692661%2C-122.230233%2047.695897%2C-122.232293%2047.699132%2C-122.235040%2047.701904%2C-122.237099%2047.704677%2C-122.239846%2047.707449%2C-122.242593%2047.710221%2C-122.244653%2047.712994%2C-122.246713%2047.715304%2C-122.248772%2047.717613%2C-122.250832%2047.719923%2C-122.252206%2047.721771%2C-122.253579%2047.723619%2C-122.254952%2047.725004%2C-122.256326%2047.726390%2C-122.257699%2047.727314%2C-122.258385%2047.728238%2C-122.259072%2047.729161%2C-122.259759%2047.730085%2C-122.260445%2047.730547%2C-122.261132%2047.731471%2C-122.261819%2047.731932%2C-122.262505%2047.732394%2C-122.263192%2047.733318%2C-122.263879%2047.733780%2C-122.264565%2047.734242%2C-122.265252%2047.734703%2C-122.265939%2047.735165%2C-122.266625%2047.735627%2C-122.267312%2047.736089%2C-122.267999%2047.736551%2C-122.268685%2047.737012%2C-122.270058%2047.737936%2C-122.270745%2047.738859%2C-122.271432%2047.739783%2C-122.272118%2047.740245%2C-122.272805%2047.740707%2C-122.273492%2047.741168%2C-122.274178%2047.741168%2C-122.274865%2047.741630%2C-122.275552%2047.741630%2C-122.278298%2047.739783&v=8&zoomLevel=11'
    return endpoint

def main():
    base_url = 'https://www.redfin.com/stingray/api/'
    endpoint = get_endpoint_from_args()
    data: List[Property] = scrape_redfin(base_url + endpoint)
    if len(data) > 0:
        print(data)

if __name__ == '__main__':
    main()



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