import requests
from ambiance import Atmosphere 

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


