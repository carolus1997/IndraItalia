import arcpy
import os
import re

arcpy.env.overwriteOutput = True

# Define las rutas de las capas de entrada, la capa de provincias y el geodatabase de salida
capa_entrada = input("Introduce la ruta de la capa a recortar: ")
capa_provincias = input("Introduce la ruta de la capa de provincias: ")
gdb_output = input("Introduce la ruta de la gdb de destino: ")
gdb_salida = gdb_output

# Crea una capa temporal de la capa de provincias
arcpy.MakeFeatureLayer_management(capa_provincias, 'provincias_lyr')

# Obtiene una lista de las provincias en la capa de provincias
provincias = [row[0] for row in arcpy.da.SearchCursor('provincias_lyr', 'NAME_2')]

# Sustituye las comillas simples en los nombres de las provincias por un carácter de escape de comilla simple
provincias_escaped = [provincia.replace("'", "_") for provincia in provincias]

print(f"LISTA DE PRONVINCIAS: {provincias_escaped}")

# Recorre cada provincia
for provincia in provincias_escaped:
    # Selecciona la provincia actual
    arcpy.SelectLayerByAttribute_management('provincias_lyr', 'NEW_SELECTION', f"NAME_2 = '{provincia}'")

    # Define el nombre de la capa de salida
    nombre_capa_salida = f"rios_{provincia}"
    nombre_capa_salida = nombre_capa_salida.replace(" ", "_").replace("-", "_")
    capa_salida = os.path.join(gdb_salida, nombre_capa_salida)

    # Recorta la capa de entrada según los límites de la provincia actual y guarda el resultado en la capa de salida
    arcpy.Clip_analysis(capa_entrada, 'provincias_lyr', capa_salida)

# Elimina la capa temporal de provincias
arcpy.Delete_management('provincias_lyr')

print("PROCESO TERMINADO")

