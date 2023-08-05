from geopy.geocoders import Nominatim
import os

s_no_space = 5
address_space = 64
coordinates_space = 48

def listToString(s):
    str1 = ""
    for ele in s:
        str1 += ele + " "
    return str1

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
    location_menu_input=int(input("Enter Choice, Enter 0 to Search Again:- "))
    if location_menu_input == 0:
        location_selector()
    else:
        return dic[location_menu_input]
    
def main():
    BRlat,TLlat,TLlon,BRlon=location_selector()
    print("Coordinate Information:")
    print("Bottom Right Latitude \t= {}\nBottom Right Longitude \t= {}\nTop Left Latitude \t= {}\nTop Left Longitude \t= {}".format(BRlat,BRlon,TLlat,TLlon))
if __name__ == "__main__":
    main()