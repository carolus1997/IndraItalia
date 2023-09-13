import arcpy
import os

# Define las rutas de las geodatabases de entrada y salida y la carpeta de provincias
gdb_entrada = input("Introduce la ruta de la gdb de entrada: ")
carpeta_provincias = input("Introduce la ruta de la carpeta de provincias: ")
carpeta_salida = input("Introduce la ruta de la carpeta de salida: ")

# Lista todos los rasters en la geodatabase de entrada
arcpy.env.workspace = gdb_entrada
rasters = arcpy.ListRasters()

# Lista todas las capas de provincias en la carpeta de provincias
arcpy.env.workspace = carpeta_provincias
provincias = arcpy.ListFeatureClasses()

# Itera a través de cada raster
for raster in rasters:
    # Obtén el nombre de la provincia del nombre del raster
    nombre_provincia = raster.replace('Dem_', '')

    # Itera a través de cada provincia
    for provincia in provincias:
        # Si el nombre del raster coincide con el nombre de la provincia
        if nombre_provincia == provincia:
            try:
                # Obtiene el nombre de la región de la provincia
                nombre_region = arcpy.da.SearchCursor(provincia, 'NAME_1').next()[0]

                # Define la ruta de la geodatabase de salida
                gdb_salida = os.path.join(carpeta_salida, f"{nombre_region}.gdb")

                # Define el nombre del raster de salida
                nombre_raster_salida = f"Dem_{provincia}"
                nombre_raster_salida = nombre_raster_salida.replace(" ", "_").replace("-", "_")
                raster_salida = os.path.join(gdb_salida, nombre_raster_salida)

                # Crea una capa temporal de la capa de provincias
                arcpy.MakeFeatureLayer_management(provincia, 'provincias_lyr')

                # Selecciona la provincia actual
                arcpy.SelectLayerByAttribute_management('provincias_lyr', 'NEW_SELECTION', f"NAME_2 = '{provincia}'")

                # Recorta el raster de entrada según los límites de la provincia actual y guarda el resultado en el raster de salida
                arcpy.Clip_management(raster, "#", raster_salida, 'provincias_lyr', "#", "ClippingGeometry", "NO_MAINTAIN_EXTENT")

                # Elimina la capa temporal de provincias
                arcpy.Delete_management('provincias_lyr')

            except Exception as e:
                print(f"Error processing {provincia}: {e}")

print("PROCESO TERMINADO")

# NO FUNCIONA AUN

