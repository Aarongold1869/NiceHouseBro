from functools import lru_cache
import requests

def mls_grid_api():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", 
        "accept": "application/json",
        "content-type": "application/json"
    }
    url = 'https://api.mlsgrid.com/v2/Property?$filter=OriginatingSystemName%20eq%20%27actris%27%20and%20ModificationTimestamp%20gt%202020-12-30T23:59:59.99Z&$expand=Media,Rooms,UnitTypes'
    res = requests.get(url, headers=headers)
    print(res)
    if res.ok:
        return res.json()
    else:
        return None     


def main():
    res = mls_grid_api()
    print(res)


if __name__ == '__main__':
    main()