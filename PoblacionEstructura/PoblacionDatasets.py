import os
import arcpy
import re

arcpy.env.overwriteOutput = True

def obtener_nombre_dataset(nombre_capa):
    partes = nombre_capa.split("_")
    partes = partes[1:]  # Eliminar la primera parte de la lista
    nombre_dataset = "_".join(partes)

    # Eliminar caracteres adicionales según corresponda
    nombre_dataset = re.sub(r'_+', '_', nombre_dataset)

    return nombre_dataset

def mapear_nombre_provincia_a_dataset(nombre_provincia):
    # Reemplazar los caracteres especiales con guiones bajos
    nombre_provincia = re.sub(r'[- ]', '_', nombre_provincia)
    nombre_provincia = re.sub(r'_+', '_', nombre_provincia)

    return nombre_provincia

#  copiar raster o feature class
def copiar_recurso(origen, destino, tipo):
    if tipo == "FeatureClass":
        arcpy.CopyFeatures_management(origen, destino)
    elif tipo == "Raster":
        arcpy.CopyRaster_management(origen, destino)


# Construir las rutas completas a las carpetas
ruta_recursos = input("Introduce la ruta de la carpeta de entrada: ")
ruta_resultados = input("Introduce la ruta de la carpeta de destino: ")

tipocapa = input("Introduce el tipo de capa que vas a usar por ej. rios, carreteras, etc: ")

# Crear las carpetas de resultados si no existen
if not os.path.exists(ruta_resultados):
    os.makedirs(ruta_resultados)

# Procesar archivos en la carpeta de recursos
archivos_recurso = os.listdir(ruta_recursos)
recursos = []

try:
    for archivo in archivos_recurso:
        if archivo.endswith(".gdb"):
            gdb_origen = os.path.join(ruta_recursos, archivo)
            arcpy.env.workspace = gdb_origen
            feature_classes = arcpy.ListFeatureClasses()
            rasters = arcpy.ListRasters()

            # Agregar feature classes y rasters a la lista de recursos
            recursos.extend([(fc, "FeatureClass") for fc in feature_classes])
            recursos.extend([(raster, "Raster") for raster in rasters])
except Exception as e:
    print(f"Error al listar los recursos: {e}")

if not recursos:
    print("No se encontraron recursos en la carpeta de recursos.")
    exit()

# Procesar archivos en la carpeta de resultados
try:
    archivos_resultados = os.listdir(ruta_resultados)
    for archivo in archivos_resultados:
        if archivo.endswith(".gdb"):
            gdb_resultado = os.path.join(ruta_resultados, archivo)
            arcpy.env.workspace = gdb_resultado
            datasets = arcpy.ListDatasets("*", "Feature")
            for dataset in datasets:
                for recurso, tipo_recurso in recursos:
                    nombre_provincia_recurso = obtener_nombre_dataset(recurso)
                    if mapear_nombre_provincia_a_dataset(nombre_provincia_recurso) == dataset:
                        recurso_origen = os.path.join(gdb_origen, recurso)
                        recurso_destino = os.path.join(gdb_resultado, dataset, f"{mapear_nombre_provincia_a_dataset(nombre_provincia_recurso)}_{tipocapa}")
                        if not arcpy.Exists(recurso_destino):
                            copiar_recurso(recurso_origen, recurso_destino, tipo_recurso)
                            print(f"Se ha copiado el recurso: {recurso_destino}")
except Exception as e:
    print(f"Error durante el proceso: {e}")