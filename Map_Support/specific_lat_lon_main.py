import os
import json
from geopy.geocoders import Nominatim
from geocoding import listToString
import requests
from map_support_main import run

s_no_space = 5
address_space = 64
coordinates_space = 48

file_dir = os.path.dirname(__file__)
prefs_path = os.path.join(file_dir, 'preferences.json')

default_prefs = {
        'url': 'https://mt.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        'tile_size': 256,
        'tile_format': 'jpg',
        'dir': os.path.join(file_dir, 'images'),
        'headers': {
            'cache-control': 'max-age=0',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'
        },
        'tl': '',
        'br': '',
        'zoom': ''
    }

def call_nominatim_api(lat, lon, zoom):
    base_url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        "format": "xml",
        "lat": lat,
        "lon": lon,
        "zoom": zoom,
        "addressdetails": 1
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        return response.text
    else:
        return f"Error: {response.status_code}"

def location_selector():
    dic={}
    os.system('cls')
    geolocator = Nominatim(user_agent="Satellite_Project")
    address = input("Enter the location\n")
    location_list = geolocator.geocode(address,addressdetails=True,exactly_one=False)
    i=1  
    for location in location_list:
        if location.address is not None:
            if i==1:
                j=0
                while j < s_no_space + address_space + coordinates_space + 10:
                    print("-",end="")
                    j+=1
                print("\n| {:>5} | {:>64} | {:>48} |".format("S.No.","Address [Characters]","Coordinates"))
                j=0
                while j < s_no_space + address_space + coordinates_space + 10:
                    print("-",end="")
                    j+=1
                print("")
            addresscovered = 0
            print("| {:>5} | {:>64} | {:>48} |".format(str(i),location.address[:64],listToString([location.raw['lat'],location.raw['lon']])))
            addresscovered += 64
            while addresscovered<len(location.address):
                print("| {:>5} | {:>64} | {:>48} |".format("",location.address[addresscovered:addresscovered+64],""))
                addresscovered+=64
            dic[i]=[location.raw['lat'],location.raw['lon']]
            i=i+1
            print("| {:>5} | {:>64} | {:>48} |".format("","",""))
        else:
            print("Invalid Location Entered, try something else")
    j=0
    while j < s_no_space + address_space + coordinates_space + 10:
        print("-",end="")
        j+=1
    print("")
    location_menu_input=int(input("Enter Choice, Enter 0 to Search Again:- "))
    if location_menu_input == 0:
        location_selector()
    else:
        return dic[location_menu_input]

def main():
    print("We will work with the specific case now, huh")
    if not os.path.isfile(prefs_path):
        with open(prefs_path, 'w', encoding='utf-8') as f:
            json.dump(default_prefs, f, indent=2, ensure_ascii=False)
        print(f'Preferences file created in {prefs_path}')
        input("Press Enter")
    latitude = float(input("Enter Center Latitude:- "))
    longitude = float(input("Enter Center Longitude:- "))
    zoom_level = int(input("Enter Map Zoom Level:- "))
    
    api_response = call_nominatim_api(latitude, longitude, zoom_level)
    split_api = api_response.split()
    for x in split_api:
        if x.startswith('boundingbox='):
            ans = x
    ans = ((ans.split('='))[1]).split(',')
    BRlat = float(ans[0][1:])
    BRlon = float(ans[3][:-1])
    TLlat = float(ans[1])
    TLlon = float(ans[2])

    print("Coordinate Information:\nBottom Right Latitude\t= {}\nBottom Right Longitude\t= {}\nTop Left Latitude\t= {}\nTop Left Longitude\t= {}".format(BRlat,BRlon,TLlat,TLlon))
    detail = input("Enter the detail Level")
    run(BRlat,BRlon,TLlat,TLlon,detail)
    input("Operation Completed, Press Enter")

if __name__ == "__main__":
    main()