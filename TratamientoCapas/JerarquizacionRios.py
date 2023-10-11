import arcpy
import os

arcpy.env.overwriteOutput = True

# Ruta donde se encuentran las carpetas
ruta = input("Introduce la ruta a tu carpeta: ")  # Modifica esto con la ruta correcta

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
        capas_rios = []
        for capa in ["RIO"]:
            archivos_capa = [f for f in os.listdir(carpeta_path) if capa in f and f.endswith('.shp')]
            for archivo in archivos_capa:
                capa_path = os.path.join(carpeta_path, archivo)
                # Verificar que la capa exista y sea de tipo línea
                if arcpy.Exists(capa_path):
                    desc = arcpy.Describe(capa_path)
                    if desc.shapeType == "Polyline":
                        capas_rios.append(capa_path)
        print(f'Lista de capas de rios: {capas_rios}')

        # Realizar el Merge de las capas encontradas
        for rio in capas_rios:
            capa_resultante = os.path.join(carpeta_path, f"Rios_{carpeta}")
            arcpy.AddField_management(rio, "Jerarquia", "SHORT")

            # Usa un cursor de actualización para copiar los valores del campo texto al nuevo campo short
            with arcpy.da.UpdateCursor(rio, ['JERAR_0302', 'Jerarquia']) as cursor:
                for row in cursor:
                    try:
                        # Convierte el valor del campo "jerarquia" a short y lo asigna al nuevo campo
                        row[1] = int(row[0])
                        cursor.updateRow(row)
                    except ValueError:
                        # Si hay algún error al convertir, puedes imprimir un mensaje o simplemente pasar
                        print(f"Error al convertir el valor '{row[0]}' a short.")
                        pass
