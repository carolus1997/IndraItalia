import os
import arcpy

arcpy.env.overwriteOutput = True
def procesar_capa(nombre_capa):
    # Añadir un nuevo campo 'codigo' y 'descripcion del codigo' a la capa
    # arcpy.AddField_management(nombre_capa, "codigoTipo", "SHORT")
    # arcpy.AddField_management(nombre_capa, "desCodTip", "TEXT")

    # Diccionarios con los atributos de carreteras y vías urbanas
    atributos_carreteras = {
        "11": "AUTOPISTA PEAJE ",
        "12": "AUTOPISTA LIBRE/AUTOVÍA ",
        "21": "CARRETERA CONVENCIONAL",
        "22": "MULTICARRIL",
        "23": "ITINERARIO EUROPEO ",
        "99": "NO APLICABLE/NO DISPONIBLE"
    }
    atributos_vias_urbanas = {
        "01": "TRONCAL ",
        "10": "VÍA DE SERVICIO ",
        "11": "ROTONDA",
        "12": "ENLACE",
        "99": "NO APLICABLE/NO DISPONIBLE"
    }

    # Cambiando las claves por los valores en el diccionario atributos_carreteras
    atributos_carreteras = {v: k for k, v in atributos_carreteras.items()}

    # Cambiando las claves por los valores en el diccionario atributos_vias_urbanas
    atributos_vias_urbanas = {v: k for k, v in atributos_vias_urbanas.items()}

    with arcpy.da.UpdateCursor(nombre_capa, ["TIPO_0605", "SITUA_0622", "SITUA_0623", "SITUA_0626", "codigoTipo",
                                             "desCodTip"]) as cursor:
        for row in cursor:
            if row[0] is not None:
                #print(f"Evaluando TIPO_0605: {row[0]}")  # Debug
                if row[0] == '21':
                    row[4] = 4
                    row[5] = 'Carreretera Convencional'
                elif row[0] == '23':
                    row[4] = 4
                    row[5] = 'Itinerario Europeo'
                elif row[0] == '22':
                    row[4] = 4
                    row[5] = 'Multicarril'
                elif row[0] == '12':
                    row[4] = 5
                    row[5] = 'Autovia'
                elif row[0] == '11':
                    row[4] = 6
                    row[5] = 'Autopista'
                elif row[0] == '99':
                    row[4] = 0
                    row[5] = 'No disponible'
                cursor.updateRow(row)

            elif row[1] is not None:
                #print(f"Evaluando SITUA_0622: {row[1]}")  # Debug
                row[4] = 3
                row[5] = 'Urbana'
                cursor.updateRow(row)

            elif row[2] is not None:
                #print(f"Evaluando SITUA_0623: {row[2]}")  # Debug
                row[4] = 2
                row[5] = 'Camino'
                cursor.updateRow(row)

            elif row[3] is not None:
                #print(f"Evaluando SITUA_0626: {row[3]}")  # Debug
                row[4] = 2
                row[5] = 'Senda'
                cursor.updateRow(row)




# # Ruta donde se encuentran las carpetas
# ruta = input("Introduce la ruta a tu carpeta: ")  # Modifica esto con la ruta correcta
#
# # Lista para almacenar las capas resultantes
# capas_resultantes = []
#
# # Leer todas las carpetas en la ruta
# for carpeta in os.listdir(ruta):
#     carpeta_path = os.path.join(ruta, carpeta)
#
#     # Verificar si es una carpeta
#     if os.path.isdir(carpeta_path):
#         print(f"Verificando carpeta: {carpeta_path}")
#         # Imprimir todos los archivos en la subcarpeta
#         print("Archivos en la carpeta:", os.listdir(carpeta_path))
#         # Buscar las capas dentro de la carpeta
#         capas_a_mezclar = []
#         for capa in ["CARRETERA", "CAMINO", "SENDA", "URBANA"]:
#             # Busca archivos que contienen la palabra clave de la capa y terminan en .shp
#             archivos_capa = [f for f in os.listdir(carpeta_path) if capa in f and f.endswith('.shp')]
#             for archivo in archivos_capa:
#                 capa_path = os.path.join(carpeta_path, archivo)
#                 if arcpy.Exists(capa_path):
#                     capas_a_mezclar.append(capa_path)
#         print(f'Lista de capas a jerarquizar: {capas_a_mezclar}')
# #         # Realizar el Merge de las capas encontradas
# #         if capas_a_mezclar:
# #             capa_resultante = os.path.join(carpeta_path, f"Vias_{carpeta}")
# #             arcpy.Merge_management(capas_a_mezclar, capa_resultante)
#              capas_resultantes.append(capa_resultante)

# Llamada a la función para cada capa resultante

capas_resultantes = []

# Ruta de la carpeta principal
directory_path = r'C:\Users\ctmiraperceval\OneDrive - Indra\Escritorio\CartoItalia\Data\Recursos_Es\BTN'

# Recorrer la carpeta principal
for root, dirs, files in os.walk(directory_path):
    for file in files:
        # Buscar archivos que contengan 'Vias_' en su nombre
        if 'Vias_' in file and '.shp' in file and '.xml' not in file:
            capas_resultantes.append(os.path.join(root, file))
print(f'capas resultantes={capas_resultantes}')
for capa in capas_resultantes:
    procesar_capa(capa)
