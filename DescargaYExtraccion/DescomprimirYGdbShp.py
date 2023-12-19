import os
import zipfile
import arcpy

directorio_principal = r'C:\Users\ctmiraperceval\Desktop\CartografiaPaises\Recursos\Reursos_Chi\DEM'

for root, dirs, files in os.walk(directorio_principal):
    for archivo in files:
        if archivo.endswith('.zip'):
            ruta_completa = os.path.join(root, archivo)

            # Crear un directorio con el mismo nombre que el archivo ZIP (sin la extensión)
            directorio_destino = os.path.join(root, archivo[:-4])
            if not os.path.exists(directorio_destino):
                os.makedirs(directorio_destino)

            # Descomprimir el archivo ZIP en el directorio creado
            with zipfile.ZipFile(ruta_completa, 'r') as archivo_zip:
                archivo_zip.extractall(directorio_destino)



# nombre_gdb = "TrentoCatastro.gdb"
# ruta_gdb = os.path.join(directorio_principal, nombre_gdb)
#
# if not arcpy.Exists(ruta_gdb):
#     arcpy.CreateFileGDB_management(directorio_principal, nombre_gdb)
#
#
# shapefiles = []
#
# for root, dirs, files in os.walk(directorio_principal):
#     for archivo in files:
#         if archivo.endswith('_parcel_poly.shp'):
#             ruta_shp = os.path.join(root, archivo)
#             shapefiles.append(ruta_shp)
#
# # Fusionar los shapefiles
# merged_shp = 'merged_parcel_poly.shp'
# if not arcpy.Exists(merged_shp):
#     arcpy.arcpy.management.Merge(shapefiles, merged_shp)
#
# # Importar el shapefile fusionado a la gdb
# if not arcpy.Exists(os.path.join(ruta_gdb, merged_shp)):
#     arcpy.FeatureClassToGeodatabase_conversion(merged_shp, ruta_gdb)
