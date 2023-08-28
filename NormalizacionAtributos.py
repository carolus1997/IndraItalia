import arcpy
import os
peticionEnv= input("Introduce la ruta de tu entorno")
arcpy.env.workspace = peticionEnv
#Las capas que vamos a fusionar
peticionNombres= input("Introduce la ruta de tu entorno")
shapefiles = arcpy.ListFeatureClasses(peticionNombres)
#Aseguramos que todas esten en el mismo sistema de coordenadas
output_coordinate_system = arcpy.SpatialReference('WGS 1984')
for shapefile in shapefiles:
    arcpy.Project_management(shapefile, shapefile[:-4] + '_proj.shp', output_coordinate_system)

#Configuramos los atributos que falten
for shapefile in shapefiles:
    arcpy.AddField_management(shapefile, 'atributo', 'TEXT')

#Fusionamos las capas
arcpy.Merge_management(shapefiles, 'capa_fusionada.shp')
