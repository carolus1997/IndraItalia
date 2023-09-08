import os
import zipfile
import arcpy

directorio_principal = r'C:\Users\ctmiraperceval\Desktop\CartoItalia\Data\Recursos\Trento'

for root, dirs, files in os.walk(directorio_principal):
    for archivo in files:
        if archivo.endswith('.zip'):
            ruta_completa = os.path.join(root, archivo)
            with zipfile.ZipFile(ruta_completa, 'r') as archivo_zip:
                archivo_zip.extractall(root)



nombre_gdb = "TrentoCatastro.gdb"
ruta_gdb = os.path.join(directorio_principal, nombre_gdb)

if not arcpy.Exists(ruta_gdb):
    arcpy.CreateFileGDB_management(directorio_principal, nombre_gdb)


shapefiles = []

for root, dirs, files in os.walk(directorio_principal):
    for archivo in files:
        if archivo.endswith('_parcel_poly.shp'):
            ruta_shp = os.path.join(root, archivo)
            shapefiles.append(ruta_shp)

# Fusionar los shapefiles
merged_shp = 'merged_parcel_poly.shp'
if not arcpy.Exists(merged_shp):
    arcpy.arcpy.management.Merge(shapefiles, merged_shp)

# Importar el shapefile fusionado a la gdb
if not arcpy.Exists(os.path.join(ruta_gdb, merged_shp)):
    arcpy.FeatureClassToGeodatabase_conversion(merged_shp, ruta_gdb)
