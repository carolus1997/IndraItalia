import os
import geopandas as gpd

# Define la ruta de la carpeta de entrada y salida
input_folder = r"D:\Minsait_Curro\Recursos_Por\Edificios\GeoJSON"
output_folder = r"D:\Minsait_Curro\Recursos_Por\Edificios\GeoJSONToShp"

# Crea la carpeta de salida si no existe
os.makedirs(output_folder, exist_ok=True)

# Recorre todos los archivos en la carpeta de entrada
for filename in os.listdir(input_folder):
    # Comprueba si el archivo es un archivo GeoJSON
    if filename.endswith('.geojson'):
        # Define la ruta completa del archivo de entrada y salida
        input_file = os.path.join(input_folder, filename)
        output_file = os.path.join(output_folder, filename[:-8] + '.shp')  # Cambia la extensión a .shp

        # Lee el archivo GeoJSON en un GeoDataFrame
        gdf = gpd.read_file(input_file)

        # Escribe el GeoDataFrame a un archivo Shapefile
        gdf.to_file(output_file)
