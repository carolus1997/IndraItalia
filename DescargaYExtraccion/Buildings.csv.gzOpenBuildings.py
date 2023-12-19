import gzip
import shutil
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon
from shapely.wkt import loads
import re

def es_coordenada(valor):
    try:
        float(valor)
        return True
    except ValueError:
        return False

def detectar_geometria(df):
    columnas = df.columns

    # Buscar pares de columnas que parezcan latitud y longitud
    for col1 in columnas:
        for col2 in columnas:
            if col1 != col2 and df[col1].apply(es_coordenada).all() and df[col2].apply(es_coordenada).all():
                return 'Point'

    # Buscar columnas con formato WKT
    wkt_pattern = re.compile(r'POINT|LINESTRING|POLYGON')
    for col in columnas:
        if df[col].astype(str).str.contains(wkt_pattern).any():
            if 'POINT' in df[col].iloc[0]:
                return 'Point'
            elif 'LINESTRING' in df[col].iloc[0]:
                return 'LineString'
            elif 'POLYGON' in df[col].iloc[0]:
                return 'Polygon'

    # Si no se encuentra ningún patrón, devolver None o generar un error
    return None

# Nombres de los archivos
archivo_comprimido = r'C:\Users\ctmiraperceval\Desktop\CartografiaPaises\Recursos\Reursos_Chi\Edificios\PruebasOpenBuildings\96b_buildings.csv.gz'
archivo_csv = r"C:\Users\ctmiraperceval\Desktop\CartografiaPaises\Recursos\Reursos_Chi\Edificios\PruebasOpenBuildings\96b_buildings.csv"
archivo_shp = r"C:\Users\ctmiraperceval\Desktop\CartografiaPaises\Recursos\Reursos_Chi\Edificios\PruebasOpenBuildings\96b_buildings.shp"

# Descomprimir el archivo CSV
with gzip.open(archivo_comprimido, 'rb') as entrada:
    with open(archivo_csv, 'wb') as salida:
        shutil.copyfileobj(entrada, salida)

# Leer el archivo CSV
df = pd.read_csv(archivo_csv)

# Detectar el tipo de geometría
tipo_geometria = detectar_geometria(df)

# Crear geometrías y GeoDataFrame
if tipo_geometria == 'Point':
    # Asumiendo que hay columnas 'latitud' y 'longitud'
    gdf = gpd.GeoDataFrame(df, geometry=[Point(xy) for xy in zip(df['longitud'], df['latitud'])])
elif tipo_geometria == 'LineString':
    # Asumiendo que los LineString están en formato WKT en una columna
    gdf = gpd.GeoDataFrame(df, geometry=df['wkt_column'].apply(loads))
elif tipo_geometria == 'Polygon':
    # Asumiendo que los Polygon están en formato WKT en una columna
    gdf = gpd.GeoDataFrame(df, geometry=df['wkt_column'].apply(loads))

# Establecer el sistema de referencia de coordenadas (WGS84)
gdf.set_crs(epsg=4326, inplace=True)

# Guardar el GeoDataFrame como archivo shapefile
gdf.to_file(archivo_shp)

print(f"Archivo Shapefile guardado como: {archivo_shp}")
