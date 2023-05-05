import utm 
import pyproj
from geopy.geocoders import Nominatim
import requests
from pandas import *
global zoneVal
from ambiance import Atmosphere 

def locator(coordinates):
    try:
        geolocator = Nominatim(user_agent = "geoapiExercises")
        city = geolocator.reverse(coordinates)
        print('adding city')
    except Exception as e:
        pass

    if city.raw['address'].get('province', '')=='':
        if city.raw['address'].get('state_district', '') != '':
            province = city.raw['address'].get('state_district', '')
        else: province = city.raw['address'].get('state', '')
    else: province = city.raw['address'].get('province', '')

    match province:
        case 'Alacant / Alicante':
            province = 'Alicante'
        case 'Araba/Álava':
            province = 'Álava'
        case 'Asturias / Asturies':
            province = 'Asturias'
        case 'Comunitat Valenciana':
            province = 'Castellón'
        case 'Comunidad de Madrid':
            province = 'Madrid'
        case 'Región de Murcia':
            province = 'Murcia'
        case 'Navarra - Nafarroa':
            province = 'Navarra'
        case 'València / Valencia':
            province = 'Valencia'
        case _:
            pass 
    return province

def XY_To_LatLon(x,zoneV):
    P = pyproj.Proj(proj='utm', zone=zoneV, ellps='WGS84', preserve_units=True)
    coordinates = P(x[0],x[1],inverse=True)
    coordinates = list(coordinates)
    coordinates.reverse()
    return coordinates #latitude and longitude

def LatLon_To_XY(Lat,Lon):
    p1=pyproj.Proj('+proj=utm +zone=31, +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs'
)
    (x,y)=p1(Lat,Lon)
    return(x,y)

# # val = XY_To_LatLon((677470.77,4286991.87),30)
# pass

def latLonToXY(lat,lon):
    coordinatesUTM = utm.from_latlon(lat,lon)
    return coordinatesUTM #UTMx, UTMy, huso

# val = utm.from_latlon(41.33461,1.727867)



def get_elevationAndPressure(lat, lon):
    url = ('https://api.opentopodata.org/v1/test-dataset'f'?locations={lat},{lon}')
    while True:
        try:
           response = requests.get(url).json()
        except Exception as e:
           continue
        break
   
    elevation = response['results'][0]['elevation']
    pressure = (Atmosphere(elevation).pressure[0])*(76/101325) #in cmHg

    return elevation, pressure 


# # def get_elevationAndPressure(lat, long):
# #     query = ('https://api.open-elevation.com/api/v1/lookup'f'?locations={lat},{long}')
# #     try:
# #         r = requests.get(query).json()  # json object, various ways you can extract value
# #         elevation = io.json.json_normalize(r, 'results')['elevation'].values[0]
# #     except Exception as e:
# #         try:
# #             r = requests.get(query).json()  # json object, various ways you can extract value
# #             elevation = io.json.json_normalize(r, 'results')['elevation'].values[0]
# #         except Exception as e:
# #             elevation=500
# #     # one approach is to use pandas json functionality
    
# #     # elevation = io.json.json_normalize(r, 'results')['elevation'].values[0]
# #     # elevation = Elevation(lat, long)
# #     pressure = (Atmosphere(elevation).pressure[0])*(76/101325) #in cmHg
# #     return elevation, pressure

# val = elevation_function(32.33461,3.727867)
pass

