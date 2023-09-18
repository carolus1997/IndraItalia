import os
import arcpy

def obtener_nombre_dataset(nombre_capa, tipo_capa):
    partes = nombre_capa.split("_")
    partes = [parte for parte in partes if parte != tipo_capa]  # Eliminar la parte correspondiente al tipo de capa
    nombre_dataset = "_".join(partes)

    # Eliminar caracteres adicionales según corresponda
    nombre_dataset = nombre_dataset.replace("__", "_")
    nombre_dataset = nombre_dataset.replace("____", "_")

    return nombre_dataset

def mapear_nombre_provincia_a_dataset(nombre_provincia, tipo_capa):
    # Reemplazar los caracteres especiales con guiones bajos
    nombre_provincia = nombre_provincia.replace("-", "_")
    nombre_provincia = nombre_provincia.replace(" ", "_")
    nombre_provincia = nombre_provincia.replace("__", "_")

    # Eliminar los guiones bajos duplicados y el tipo de capa
    partes_nombre = nombre_provincia.split("_")
    partes_nombre = [parte for parte in partes_nombre if parte != "" and parte != tipo_capa]

    # Unir las partes del nombre con guiones bajos
    nombre_provincia_dataset = "_".join(partes_nombre)

    return nombre_provincia_dataset

# Obtener la cantidad de capas a manejar
num_capas = int(input("Por favor, introduzca el número de capas a manejar: "))
ruta_resultados= r"C:\Users\ctmiraperceval\OneDrive - Indra\Escritorio\CartoItalia\Data\Resultados\Gdbs"
# Obtener los detalles de cada capa
capas = []
for i in range(num_capas):
    ruta_capa = input(f"Por favor, introduzca la ruta de la gdb {i+1}: ")
    tipo_capa = input(f"Por favor, introduzca el tipo de la capa {i+1} (por ejemplo, 'Rios'): ")
    capas.append({"ruta": ruta_capa, "tipo": tipo_capa})

# Iterar sobre las capas
for capa in capas:
    # Obtener la lista de archivos en la carpeta de la capa
    archivos_capa = os.listdir(capa["ruta"])
    capas_capa = []
    if archivos_capa:
        for archivo in archivos_capa:
            if archivo.endswith(".gdb"):
                gdb_capa = os.path.join(capa["ruta"], archivo)
                arcpy.env.workspace = gdb_capa
                try:
                    capas_capa = arcpy.ListFeatureClasses()
                except arcpy.ExecuteError:
                    print(arcpy.GetMessages())
    else:
        print(f"No se encontraron archivos en la carpeta {capa['ruta']}")

    # Añadir las capas a la lista de capas de la capa actual
    capa["capas"] = capas_capa

archivos_resultados = os.listdir(ruta_resultados)
for archivo in archivos_resultados:
    if archivo.endswith(".gdb"):
        gdb_resultado = os.path.join(ruta_resultados, archivo)
        # Acceder a la geodatabase y a los datasets dentro de ella
        arcpy.env.workspace = gdb_resultado
        datasets = arcpy.ListDatasets("*", "Feature")
        for dataset in datasets:
            # Verificar si el nombre del dataset coincide con una capa de los recursos
            for capa in capas:
                for capa_capa in capa["capas"]:
                    partes_nombre = capa_capa.split("_")
                    nombre_provincia_capa = "_".join(partes_nombre[1:])
                    if mapear_nombre_provincia_a_dataset(nombre_provincia_capa, capa["tipo"]) == dataset:
                        # Copiar la capa a este dataset de resultados
                        capa_origen_capa = os.path.join(gdb_capa, capa_capa)
                        capa_destino_capa = os.path.join(gdb_resultado, dataset, f"{mapear_nombre_provincia_a_dataset(nombre_provincia_capa, capa['tipo'])}_{capa['tipo']}")
                        if not arcpy.Exists(capa_destino_capa):
                            try:
                                arcpy.CopyFeatures_management(capa_origen_capa, capa_destino_capa)
                            except arcpy.ExecuteError:
                                print(arcpy.GetMessages())