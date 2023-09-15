import arcpy
import os
import re
# Establecer la ubicación de la capa "regiones" y la capa "provincias"
regiones_layer = r"C:\Users\ctmiraperceval\OneDrive - Indra\Escritorio\CartoItalia\Data\Recursos\Unidades_Admin_It\RegionesItalia.shp"
provincias_layer = r"C:\Users\ctmiraperceval\OneDrive - Indra\Escritorio\CartoItalia\Data\Recursos\Edificios\ProvinciasItalia.shp"

# Obtener la lista de nombres de regiones de la capa "regiones"
nombres_regiones = []
with arcpy.da.SearchCursor(regiones_layer, "Name_1") as cursor:
    for row in cursor:
        nombre_region = row[0]
        nombres_regiones.append(nombre_region)

# Crear una geodatabase para cada nombre de región
output_folder = r"C:\Users\ctmiraperceval\OneDrive - Indra\Escritorio\CartoItalia\Data\Recursos\PruebasSolucionErrores\Edificios"
for nombre_region in nombres_regiones:
    # Reemplazar caracteres inválidos en el nombre de la región
    nombre_region_clean = re.sub(r"[^\w\s]", "", nombre_region)
    nombre_region_clean = nombre_region_clean.replace(" ", "_")

    gdb_name = nombre_region_clean + ".gdb"
    gdb_path = os.path.join(output_folder, gdb_name)
    arcpy.CreateFileGDB_management(output_folder, gdb_name)

    # Crear un dataset de entidades en la geodatabase correspondiente
    with arcpy.da.SearchCursor(provincias_layer, ["Name_1", "Name_2"]) as cursor:
        for row in cursor:
            nombre_region_provincia = row[0]
            nombre_provincia = row[1]
            if nombre_region_provincia == nombre_region:
                # Reemplazar caracteres inválidos en el nombre de la provincia
                nombre_provincia_clean = re.sub(r"[^\w\s]", "", nombre_provincia)
                nombre_provincia_clean = nombre_provincia_clean.replace(" ", "_")

                dataset_name = nombre_provincia_clean
                arcpy.CreateFeatureDataset_management(gdb_path, dataset_name, spatial_reference=4326)
