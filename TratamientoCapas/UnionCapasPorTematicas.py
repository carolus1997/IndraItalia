import os
import arcpy

arcpy.env.overwriteOutput = True
# Ruta donde se encuentran las carpetas
ruta = input("Introduce la ruta a tu carpeta: ")  # Modifica esto con la ruta correcta
ruta_destino= input("Introduce la ruta de la carpeta de guardado: ")
# Lista para almacenar las capas resultantes
capas_resultantes = []

# Leer todas las carpetas en la ruta
for carpeta in os.listdir(ruta):
    carpeta_path = os.path.join(ruta, carpeta)

    # Verificar si es una carpeta
    if os.path.isdir(carpeta_path):
        print(f"Verificando carpeta: {carpeta_path}")
        # Imprimir todos los archivos en la subcarpeta
        print("Archivos en la carpeta:", os.listdir(carpeta_path))
        # Buscar las capas dentro de la carpeta
        capas_a_mezclar = []
# Añade las capas
        for capa in ["BTN0305L_CAU_ART", "BTN0549L_ACUEDU"]:
            # Busca archivos que contienen la palabra clave de la capa y terminan en .shp
            archivos_capa = [f for f in os.listdir(carpeta_path) if capa in f and f.endswith('.shp')]
            for archivo in archivos_capa:
                capa_path = os.path.join(carpeta_path, archivo)
                if arcpy.Exists(capa_path):
                    capas_a_mezclar.append(capa_path)
        print(f'Lista de capas a jerarquizar: {capas_a_mezclar}')
        # Realizar el Merge de las capas encontradas
        if capas_a_mezclar:
            capa_resultante = os.path.join(ruta_destino, f"CanalesArtificiales_{carpeta}")
            arcpy.Merge_management(capas_a_mezclar, capa_resultante)

