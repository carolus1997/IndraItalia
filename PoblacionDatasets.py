import os
import arcpy

# Obtener la ruta inicial del usuario
ruta_inicial = r"C:\Users\ctmiraperceval\Desktop\CartoItalia\Data"

# Construir las rutas completas a las carpetas de ríos y carreteras
ruta_recursos_rios = os.path.join(ruta_inicial, "Recursos", "Rios")
ruta_recursos_carreteras = os.path.join(ruta_inicial, "Recursos", "Carreteras")
ruta_resultados = os.path.join(ruta_inicial, "Resultados", "Gdbs")

# Crear las carpetas de resultados si no existen
if not os.path.exists(ruta_resultados):
    os.makedirs(ruta_resultados)

# Obtener la lista de archivos en la carpeta de ríos
archivos_rios = os.listdir(ruta_recursos_rios)
if archivos_rios:
    for archivo in archivos_rios:
        if archivo.endswith(".gdb"):
            gdb_rio = os.path.join(ruta_recursos_rios, archivo)
            arcpy.env.workspace=gdb_rio
            capas_rios = arcpy.ListFeatureClasses()

else:
    print("No se encontraron archivos en la carpeta de ríos.")

# Obtener la lista de archivos en la carpeta de carreteras
archivos_carreteras = os.listdir(ruta_recursos_carreteras)
if archivos_carreteras:
    for archivo in archivos_carreteras:
        if archivo.endswith(".gdb"):
            gdb_carretera = os.path.join(ruta_recursos_carreteras, archivo)
            arcpy.env.workspace = gdb_carretera
            capas_carreteras = arcpy.ListFeatureClasses()

else:
    print("No se encontraron archivos en la carpeta de carreteras.")

archivos_resultados = os.listdir(ruta_resultados)
for archivo in archivos_resultados:
    if archivo.endswith(".gdb"):
        gdb_resultado = os.path.join(ruta_resultados, archivo)
        # Acceder a la geodatabase y a los datasets dentro de ella
        arcpy.env.workspace = gdb_resultado
        datasets = arcpy.ListDatasets("*", "Feature")
        for dataset in datasets:
            # Verificar si el nombre del dataset coincide con una capa de carreteras o ríos
            for rio in capas_rios:
                nombre_provincia_rios = rio.split("_")[1]
            for carretera in capas_carreteras:
                nombre_provincia_carreteras = carretera.split("_")[1]
            if nombre_provincia_rios == dataset or nombre_provincia_carreteras == dataset:
                # Copiar la capa a este dataset de resultados
                capa_origen = os.path.join(ruta_recursos_carreteras, dataset + ".gdb", dataset)
                capa_destino = os.path.join(gdb_resultado, dataset)
                arcpy.CopyFeatures_management(capa_origen, capa_destino)
# FALTA CUADRAR LAS ULTIMAS 3 LINEAS