import arcpy
peticionEnv = input("Introduce la ruta de tu entorno")
arcpy.env.workspace = peticionEnv
# Las capas que vamos a fusionar
peticionNombres = input("Introduce el nombre común de las capas a fusionar")
shapefiles = []
clases = arcpy.ListFeatureClasses("r"+peticionEnv)
for clase in clases:
    if peticionNombres in clases:
        shapefile = clase.name
        shapefiles.append(shapefile)
# Aseguramos que todas esten en el mismo sistema de coordenadas
output_coordinate_system = arcpy.SpatialReference('WGS 1984')
for shapefile in shapefiles:
    arcpy.Project_management(shapefile, shapefile[:-4] + '_proj.shp', output_coordinate_system)
    print("hecho")
# Configuramos los atributos que falten
# for shapefile in shapefiles:
    # arcpy.AddField_management(shapefile, 'atributo', 'TEXT')
# Fusionamos las capas
# arcpy.Merge_management(shapefiles, 'capa_fusionada.shp')
