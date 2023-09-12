import os
import arcpy

arcpy.env.overwriteOutput = True

def obtener_nombre_dataset(nombre_capa):
    partes = nombre_capa.split("_")
    partes = partes[1:]  # Eliminar la primera parte de la lista (en este caso, "rios")
    nombre_dataset = "_".join(partes)

    # Eliminar caracteres adicionales según corresponda
    nombre_dataset = nombre_dataset.replace("__", "_")
    nombre_dataset = nombre_dataset.replace("____", "_")

    return nombre_dataset
def mapear_nombre_provincia_a_dataset(nombre_provincia):
    # Reemplazar los caracteres especiales con guiones bajos
    nombre_provincia = nombre_provincia.replace("-", "_")
    nombre_provincia = nombre_provincia.replace(" ", "_")
    nombre_provincia = nombre_provincia.replace("__", "_")

    # Eliminar los guiones bajos duplicados
    partes_nombre = nombre_provincia.split("_")
    partes_nombre = [parte for parte in partes_nombre if parte != ""]

    # Unir las partes del nombre con guiones bajos
    nombre_provincia_dataset = "_".join(partes_nombre)

    return nombre_provincia_dataset



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
capas_rios = []
if archivos_rios:
    for archivo in archivos_rios:
        if archivo.endswith(".gdb"):
            gdb_rio = os.path.join(ruta_recursos_rios, archivo)
            arcpy.env.workspace = gdb_rio
            try:
                capas_rios = arcpy.ListFeatureClasses()
            except arcpy.ExecuteError:
                print(arcpy.GetMessages())
else:
    print("No se encontraron archivos en la carpeta de ríos.")

# Obtener la lista de archivos en la carpeta de carreteras
archivos_carreteras = os.listdir(ruta_recursos_carreteras)
capas_carreteras = []
if archivos_carreteras:
    for archivo in archivos_carreteras:
        if archivo.endswith(".gdb"):
            gdb_carretera = os.path.join(ruta_recursos_carreteras, archivo)
            arcpy.env.workspace = gdb_carretera
            try:
                capas_carreteras = arcpy.ListFeatureClasses()
            except arcpy.ExecuteError:
                print(arcpy.GetMessages())
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
                partes_nombre = rio.split("_")
                nombre_provincia_rios = "_".join(partes_nombre[1:])
                if mapear_nombre_provincia_a_dataset(nombre_provincia_rios) == dataset:
                    # Copiar la capa a este dataset de resultados
                    capa_origen_rios = os.path.join(gdb_rio, rio)
                    capa_destino_rios = os.path.join(gdb_resultado, dataset, f"{mapear_nombre_provincia_a_dataset(nombre_provincia_rios)}_rios")
                    if not arcpy.Exists(capa_destino_rios):
                        try:
                            arcpy.CopyFeatures_management(capa_origen_rios, capa_destino_rios)
                        except arcpy.ExecuteError:
                            print(arcpy.GetMessages())
            for carretera in capas_carreteras:
                partes_nombre = carretera.split("_")
                nombre_provincia_carreteras = "_".join(partes_nombre[1:])
                if mapear_nombre_provincia_a_dataset(nombre_provincia_carreteras) == dataset:
                    # Copiar la capa a este dataset de resultados
                    capa_origen_carreteras = os.path.join(gdb_carretera, carretera)
                    capa_destino_carreteras = os.path.join(gdb_resultado, dataset, f"{mapear_nombre_provincia_a_dataset(nombre_provincia_carreteras)}_carreteras")
                    if not arcpy.Exists(capa_destino_carreteras):
                        try:
                            arcpy.CopyFeatures_management(capa_origen_carreteras, capa_destino_carreteras)
                        except arcpy.ExecuteError:
                            print(arcpy.GetMessages())
