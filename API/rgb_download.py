import json
import re
import cv2
import requests
import numpy as np
import threading
from geopy.geocoders import Nominatim
import os

# Variables:- Formatting Space Lengths, Default Preferences for download.
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

# Function:- Convert List to Space Separated String
# Input:- List to be converted.
# Return:- Space separated elements string.
def listToString(list):
    str1 = ""
    for ele in list:
        str1 += ele + " "
    return str1

# Function:- Print List of locations present in location_list in a well-formatted manner
# Input:- Location List having several attributes (including coordinates and address)
# Output:- Prints the location in a well formatted manner.
# Return:- Dictionary containing information for all locations. 
def print_list(location_list):
    dic={}
    os.system('cls')
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
            print("| {:>5} | {:>64} | {:>48} |".format(str(i),location.address[:64],listToString(location.raw['boundingbox'])))
            addresscovered += 64
            while addresscovered<len(location.address):
                print("| {:>5} | {:>64} | {:>48} |".format("",location.address[addresscovered:addresscovered+64],""))
                addresscovered+=64
            dic[i]=location.raw['boundingbox']
            i=i+1
            print("| {:>5} | {:>64} | {:>48} |".format("","",""))
        else:
            print("Invalid Location Entered, try something else")
    j=0
    while j < s_no_space + address_space + coordinates_space + 10:
        print("-",end="")
        j+=1
    print("")
    return dic

# Function:- Location Selector responsible for searching for location coordinates based on user input.
# Input:- No Input, user is asked for input during runtime.
# Output:- Prints the Locations in a formatted manner, calls print_list.
# Return:- Return Specific Location information based on user input.
def location_selector():
    dic={}
    os.system('cls')
    geolocator = Nominatim(user_agent="Satellite_Project")
    address = input("Enter the location\n")
    location_list = geolocator.geocode(address,addressdetails=True,exactly_one=False)
    if len(location_list)==0:
        input("Empty List, Press Enter to Exit")
        return -1
    dic=print_list(location_list)
    location_menu_input=int(input("Enter Choice, Enter 0 to Search Again:- "))
    while location_menu_input > len(location_list):
        dic=print_list(location_list)
        location_menu_input=int(input("Wrong Choice, Enter 0 to Search Again or enter a valid answer:- "))
    if location_menu_input == 0:
        location_selector()
    else:
        return dic[location_menu_input]

# Support Function, API user should not use. This is used by other functions for functioning.
def download_tile(url, headers, channels):
    response = requests.get(url, headers=headers)
    arr =  np.asarray(bytearray(response.content), dtype=np.uint8)
    
    if channels == 3:
        return cv2.imdecode(arr, 1)
    return cv2.imdecode(arr, -1)

# Support Function, API user should not use. This is used by other functions for functioning.
def project_with_scale(lat, lon, scale):
    siny = np.sin(lat * np.pi / 180)
    siny = min(max(siny, -0.9999), 0.9999)
    x = scale * (0.5 + lon / 360)
    y = scale * (0.5 - np.log((1 + siny) / (1 - siny)) / (4 * np.pi))
    return x, y

"""
    Support Function, API user should not use. This is used by other functions for functioning.
    Downloads a map region. Returns an image stored either in BGR or BGRA as a `numpy.ndarray`.
    Parameters
    ----------
    `(lat1, lon1)` - Coordinates (decimal degrees) of the top-left corner of a rectangular area
    `(lat2, lon2)` - Coordinates (decimal degrees) of the bottom-right corner of a rectangular area
    `zoom` - Zoom level
    `url` - Tile URL with {x}, {y} and {z} in place of its coordinate and zoom values
    `headers` - Dictionary of HTTP headers
    `tile_size` - Tile size in pixels
    `channels` - Number of channels in the output image. Use 3 for JPG or PNG tiles and 4 for PNG tiles.
"""
def download_image(lat1: float, lon1: float, lat2: float, lon2: float,zoom: int, url: str, headers: dict, tile_size: int = 256, channels: str = 3) -> np.ndarray:
    scale = 1 << zoom

    # Find the pixel coordinates and tile coordinates of the corners
    tl_proj_x, tl_proj_y = project_with_scale(lat1, lon1, scale)
    br_proj_x, br_proj_y = project_with_scale(lat2, lon2, scale)

    tl_pixel_x = int(tl_proj_x * tile_size)
    tl_pixel_y = int(tl_proj_y * tile_size)
    br_pixel_x = int(br_proj_x * tile_size)
    br_pixel_y = int(br_proj_y * tile_size)

    tl_tile_x = int(tl_proj_x)
    tl_tile_y = int(tl_proj_y)
    br_tile_x = int(br_proj_x)
    br_tile_y = int(br_proj_y)

    img_w = abs(tl_pixel_x - br_pixel_x)
    img_h = br_pixel_y - tl_pixel_y
    img = np.ndarray((img_h, img_w, channels), np.uint8)

    def build_row(row_number):
        for j in range(tl_tile_x, br_tile_x + 1):
            tile = download_tile(url.format(x=j, y=row_number, z=zoom), headers, channels)

            # Find the pixel coordinates of the new tile relative to the image
            tl_rel_x = j * tile_size - tl_pixel_x
            tl_rel_y = row_number * tile_size - tl_pixel_y
            br_rel_x = tl_rel_x + tile_size
            br_rel_y = tl_rel_y + tile_size

            # Define where the tile will be placed on the image
            i_x_l = max(0, tl_rel_x)
            i_x_r = min(img_w + 1, br_rel_x)
            i_y_l = max(0, tl_rel_y)
            i_y_r = min(img_h + 1, br_rel_y)

            # Define how border tiles are cropped
            cr_x_l = max(0, -tl_rel_x)
            cr_x_r = tile_size + min(0, img_w - br_rel_x)
            cr_y_l = max(0, -tl_rel_y)
            cr_y_r = tile_size + min(0, img_h - br_rel_y)

            img[i_y_l:i_y_r, i_x_l:i_x_r] = tile[cr_y_l:cr_y_r, cr_x_l:cr_x_r]

    threads = []
    for i in range(tl_tile_y, br_tile_y + 1):
        thread = threading.Thread(target=build_row, args=[i])
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()
    
    return img

# Support Function, API user should not use. This is used by other functions for functioning.
# Calculates the size of an image without downloading it. Returns a `(width, height)` tuple.
def image_size(lat1: float, lon1: float, lat2: float,lon2: float, zoom: int, tile_size: int = 256):
    scale = 1 << zoom
    tl_proj_x, tl_proj_y = project_with_scale(lat1, lon1, scale)
    br_proj_x, br_proj_y = project_with_scale(lat2, lon2, scale)

    tl_pixel_x = int(tl_proj_x * tile_size)
    tl_pixel_y = int(tl_proj_y * tile_size)
    br_pixel_x = int(br_proj_x * tile_size)
    br_pixel_y = int(br_proj_y * tile_size)
    return abs(tl_pixel_x - br_pixel_x), br_pixel_y - tl_pixel_y

# Support Function, API user should not use. This is used by other functions for functioning.
# Function responsible for working with coordinate based image downloading
def run(BRlat,BRlon,TLlat,TLlon,zoom,name):
    with open(os.path.join(file_dir, 'preferences.json'), 'r', encoding='utf-8') as f:
        prefs = json.loads(f.read())

    if not os.path.isdir(prefs['dir']):
        os.mkdir(prefs['dir'])

    if (prefs['tl'] == '') or (prefs['br'] == '') or (prefs['zoom'] == ''):
        inputs = [str(TLlat)+','+str(TLlon),str(BRlat)+','+str(BRlon),str(zoom)]
        if inputs is None:
            return
        else:
            prefs['tl'], prefs['br'], prefs['zoom'] = inputs

    lat1, lon1 = re.findall(r'[+-]?\d*\.\d+|d+', prefs['tl'])
    lat2, lon2 = re.findall(r'[+-]?\d*\.\d+|d+', prefs['br'])

    zoom = int(prefs['zoom'])
    lat1 = float(lat1)
    lon1 = float(lon1)
    lat2 = float(lat2)
    lon2 = float(lon2)

    if prefs['tile_format'].lower() == 'png':
        channels = 4
    else:
        channels = 3
    img = download_image(lat1, lon1, lat2, lon2, zoom, prefs['url'],
        prefs['headers'], prefs['tile_size'], channels)

    cv2.imwrite(os.path.join(prefs['dir'], name), img)
    print(f'Saved as {name}')
    return img

# Function:- Creation/Initialization of preferences file
# Input:- User Preferences in form of Dictionary else default_prefs will be initialized.
# Return:- Returns preferences initialized in form of dictionary.
def create_prefs_file(perf_dict_name = default_prefs):
    with open(prefs_path, 'w', encoding='utf-8') as f:
        json.dump(perf_dict_name, f, indent=2, ensure_ascii=False)
    print(f'Preferences file created in {prefs_path}')
    return perf_dict_name

# Function:- Triggering location selector works on the coordinate information of the user input address.
# Input:- Output File Name
# Output:- Prints Coordinate Information
# Return:- Image array to the caller function.
def location_select_and_download(output_file_name):
    if os.path.isfile(prefs_path):
        pass
    else:
        create_prefs_file()

    BRlat, TLlat, TLlon, BRlon = location_selector()
    print("Coordinate Information:")
    print(f"Bottom Right Latitude \t= {BRlat}\nBottom Right Longitude \t= {BRlon}\nTop Left Latitude \t= {TLlat}\nTop Left Longitude \t= {TLlon}")

    zoom = input("Enter the Zoom Level:- ")
    return run(BRlat, BRlon, TLlat, TLlon, zoom,output_file_name)

# Function:- Triggering location selector works on the coordinate information of the user input coordinates.
# BR:- Bottom Right, TL mean Top Left, Lat:- Latitude and Lon:- Longitude
# Input:- BRlat,BRlon, TLlat, TLlon, Zoom, Output File Name
# Output:- Prints Coordinate Information
# Return:- Image array to the caller function.
def specific_coordinate(BRlat,BRlon, TLlat, TLlon, zoom,output_file_name):
    if os.path.isfile(prefs_path):
        pass
    else:
        create_prefs_file()
    print("Coordinate Information:")
    print(f"Bottom Right Latitude \t= {BRlat}\nBottom Right Longitude \t= {BRlon}\nTop Left Latitude \t= {TLlat}\nTop Left Longitude \t= {TLlon}")
    return run(BRlat, BRlon, TLlat, TLlon, zoom,output_file_name)

# Function:- Triggering location selector works on the coordinate information of the user input address.
# Input:- Address
# Return:- List of all locations.
def obtain_location_list(address):
    geolocator = Nominatim(user_agent="Satellite_Project")
    location_list = geolocator.geocode(address,addressdetails=True,exactly_one=False)
    if len(location_list)==0:
        input("Empty List, Press Enter to Exit")
        return -1
    else:
        return location_list