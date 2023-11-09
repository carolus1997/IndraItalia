import requests
import time
import json
import geopandas as gpd
from shapely.geometry import Point

# Función que realiza la geocodificación usando Nominatim (asegúrate de respetar sus Términos de Uso)
def geocode_using_nominatim(address):
    NOMINATIM_API_URL = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': address,
        'format': 'json'
    }
    headers = {
        'User-Agent': 'your_email@example.com' # Cambiar por tu correo electrónico
    }
    response = requests.get(NOMINATIM_API_URL, params=params, headers=headers)
    data = response.json()
    return data[0]['lat'], data[0]['lon'] if data else None, None

# Leer el JSON generado en el paso anterior
with open('datos_excel.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Lista para almacenar las entidades GeoJSON
geojson_features = []

for entry in data:
    address = f"{entry['road']} {entry['house_number']}, {entry['city']}, {entry['county']}, {entry['postcode']}, {entry['country']}"
    lat, lon = geocode_using_nominatim(address)
    if lat and lon:
        # Crear un punto con las coordenadas
        point = Point(float(lon), float(lat))
        # Añadir el punto y los atributos al GeoDataFrame
        geojson_features.append({'geometry': point, 'properties': entry})

    time.sleep(1) # Respeta la política de uso de Nominatim

# Crear GeoDataFrame
gdf = gpd.GeoDataFrame(geojson_features)

# Guardar como archivo SHP
gdf.to_file('resultado_geocodificado.shp')
