import arcpy

# Define las rutas de las capas de entrada y la capa de salida
capa1 = 'ruta/capa1.shp'
capa2 = 'ruta/capa2.shp'
capa_salida = 'ruta/capa_salida.shp'

# Realiza la intersección de las capas de entrada
arcpy.Intersect_analysis([capa1, capa2], capa_salida, "ALL", "", "INPUT")

# Selecciona los polígonos de la capa 1 que no tienen intersección
arcpy.SelectLayerByLocation_management(capa1, "SHARE_A_LINE_SEGMENT_WITH", capa2, invert_spatial_relationship=True)

# Crea una copia de los polígonos seleccionados en una nueva capa
arcpy.CopyFeatures_management(capa1, capa_salida)

# Imprime un mensaje de finalización
print("Intersección completada")
