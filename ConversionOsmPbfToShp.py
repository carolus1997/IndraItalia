import os
from osgeo import ogr

# Define la ruta del archivo de entrada y salida
#Agregar listas de capas y archivos de la carpeta de datos con un input
#modificar el codigo para usarlo en arcGIS
input_file = "/ruta/a/tu/archivo.osm.pbf"
output_file_base = "/ruta/a/tu/archivo"

# Abre el archivo de entrada
driver = ogr.GetDriverByName('OSM')
data_source = driver.Open(input_file, 0)

# Copia los datos del archivo de entrada al de salida
in_layer = data_source.GetLayer()

# Crea un diccionario para almacenar las capas de salida por tipo de geometría
out_layers = {}

for feature in in_layer:
    # Obtiene el tipo de geometría de la característica
    geom_type = feature.GetGeometryRef().GetGeometryType()

    # Crea una nueva capa para cada tipo de geometría, si aún no existe
    if geom_type not in out_layers:
        # Crea el archivo de salida
        output_file = f"{output_file_base}_{geom_type}.shp"
        out_driver = ogr.GetDriverByName('ESRI Shapefile')
        if os.path.exists(output_file):
            out_driver.DeleteDataSource(output_file)
        out_data_source = out_driver.CreateDataSource(output_file)

        out_layer = out_data_source.CreateLayer('osm_data', geom_type=geom_type)
        out_layer.CreateFields(in_layer.schema)

        out_layers[geom_type] = out_layer

    # Copia la característica a la capa de salida
    out_layers[geom_type].CreateFeature(feature)

# Cierra los archivos
data_source = None
for out_layer in out_layers.values():
    out_layer = None
