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

# Obtener la ruta inicial del usuario
ruta_inicial = r"C:\Users\ctmiraperceval\OneDrive - Indra\Escritorio\CartoItalia\Data"

# Construir las rutas completas a las carpetas
ruta_recursos = os.path.join(ruta_inicial, "Recursos_Por", "Carreteras")
ruta_resultados = os.path.join(ruta_inicial, "Resultados", "Gdbs_Por")

tipocapa = input("Introduce el tipo de capa que vas a usar por ej. rios, carreteras, etc: ")
# Crear las carpetas de resultados si no existen
if not os.path.exists(ruta_resultados):
    os.makedirs(ruta_resultados)

# Obtener la lista de archivos en la carpeta de ríos
archivos_recurso = os.listdir(ruta_recursos)
capas_recurso = []

try:
    for archivo in archivos_recurso:
        if archivo.endswith(".gdb"):
            gdb_origen = os.path.join(ruta_recursos, archivo)
            arcpy.env.workspace = gdb_origen
            capas = arcpy.ListFeatureClasses()
            if capas:
                capas_recurso.extend(capas)
except Exception as e:
    print(f"Error al listar las capas: {e}")

if not capas_recurso:
    print("No se encontraron capas en la carpeta de recursos.")
    exit()  # Terminar el script si no hay capas

try:
    archivos_resultados = os.listdir(ruta_resultados)
    for archivo in archivos_resultados:
        if archivo.endswith(".gdb"):
            gdb_resultado = os.path.join(ruta_resultados, archivo)
            arcpy.env.workspace = gdb_resultado
            datasets = arcpy.ListDatasets("*", "Feature")
            for dataset in datasets:
                for capa in capas_recurso:
                    nombre_provincia_capa = obtener_nombre_dataset(capa)
                    if mapear_nombre_provincia_a_dataset(nombre_provincia_capa) == dataset:
                        capa_origen = os.path.join(gdb_origen, capa)
                        capa_destino = os.path.join(gdb_resultado, dataset, f"{mapear_nombre_provincia_a_dataset(nombre_provincia_capa)}_{tipocapa}")
                        if not arcpy.Exists(capa_destino):
                            arcpy.CopyFeatures_management(capa_origen, capa_destino)
                            print(f"Se ha copiado la capa: {capa_destino}")
except Exception as e:
    print(f"Error durante el proceso: {e}")
