import arcpy

# Define las rutas de las capas de entrada, la capa de provincias y el geodatabase de salida
capa_entrada = input("Introduce la ruta de la capa a recortar: ")
capa_provincias = input("Introduce la ruta de la capa de provincias: ")
gdb_salida = 'ruta/gdb_salida.gdb'

# Crea una capa temporal de la capa de provincias
arcpy.MakeFeatureLayer_management(capa_provincias, 'provincias_lyr')

# Obtiene una lista de las provincias en la capa de provincias
provincias = [row[0] for row in arcpy.da.SearchCursor('provincias_lyr', 'NAME_2')]

# Recorre cada provincia
for provincia in provincias:
    # Selecciona la provincia actual
    arcpy.SelectLayerByAttribute_management('provincias_lyr', 'NEW_SELECTION', f"NAME_2 = '{provincia}'")

    # Define el nombre de la capa de salida
    capa_salida = f"{gdb_salida}/capa_entrada_{provincia}"

    # Recorta la capa de entrada según los límites de la provincia actual y guarda el resultado en la capa de salida
    arcpy.Clip_analysis(capa_entrada, 'provincias_lyr', capa_salida)

# Elimina la capa temporal de provincias
arcpy.Delete_management('provincias_lyr')
