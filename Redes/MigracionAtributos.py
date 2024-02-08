import arcpy
import os
import glob
import random
import math
import config
def generar_id_unico():
    """Genera un ID único de 10 dígitos como cadena."""
    return str(random.randint(1000000000, 9999999999))

def calcular_longitud_linea(inicio, fin):
    """Calcula la longitud de una línea dadas las coordenadas de inicio y fin."""
    return round(math.sqrt((fin[0] - inicio[0]) ** 2 + (fin[1] - inicio[1]) ** 2), 2)

def listar_campos_y_tipos(feature_class):
    # Obtener la lista de campos usando arcpy.ListFields
    campos = arcpy.ListFields(feature_class)

    # Imprimir el nombre del campo, tipo y su índice
    #for indice, campo in enumerate(campos):
        #print(f"Índice: {indice}, Campo: {campo.name}, Tipo: {campo.type}")

def actualizar_campos(feature_class):
    # Definir los campos a usar en el cursor, reemplazar 'campo_a_verificar' y los nombres de campo específicos según sea necesario
    campos = ["id", "r", "x", "imax", "unidad"]

    with arcpy.da.UpdateCursor(feature_class, campos) as cursor:
        for row in cursor:
            # Verificar si el campo específico (por ejemplo, 'campo_a_verificar') es igual a un espacio en blanco
            if row[0] == ' ':
                row[1] = 0.36  # Actualizar 'r'
                row[2] = 0.01  # Actualizar 'x'
                row[3] = 160  # Actualizar 'imax'
                row[4] = 'ohm/km'  # Actualizar 'unidad'
                cursor.updateRow(row)  # No olvides actualizar la fila en la base de datos


def obtener_vertices_tramos(feature_class):
    # Diccionario para almacenar los resultados
    tramos_dict = {}

    # Especificar los campos necesarios, incluyendo SHAPE@ para acceder a la geometría
    campos = ['id', 'SHAPE@']

    with arcpy.da.SearchCursor(feature_class, campos) as cursor:
        for row in cursor:
            id_tramo = row[0]
            # Acceder a los puntos inicial y final de la línea
            punto_inicial = row[1].firstPoint
            punto_final = row[1].lastPoint
            # Almacenar las coordenadas en el diccionario
            tramos_dict[id_tramo] = {'Inicio': (punto_inicial.X, punto_inicial.Y),
                                     'Final': (punto_final.X, punto_final.Y)}

    return tramos_dict

def obtener_info_puntos_cctt(puntos_feature_class):
    # Diccionario para almacenar los resultados
    puntos_dict = {}

    # Especificar los campos necesarios, incluyendo SHAPE@XY para acceder a las coordenadas
    campos = ['idcd', 'matricula', 'SHAPE@XY']

    with arcpy.da.SearchCursor(puntos_feature_class, campos) as cursor:
        for row in cursor:
            idcd_punto = row[0]
            matricula = row[1]
            coordenadas = row[2]  # Esto devuelve una tupla (x, y)
            # Almacenar las coordenadas y matricula en el diccionario
            puntos_dict[idcd_punto] = {'Coordenadas': coordenadas, 'Matricula': matricula}

    return puntos_dict

def obtener_info_nudos(nudos_feature_class):
    # Diccionario para almacenar los resultados
    puntos_dict = {}

    # Especificar los campos necesarios, incluyendo SHAPE@XY para acceder a las coordenadas
    campos = ['id', 'tiponudo', 'SHAPE@XY']

    with arcpy.da.SearchCursor(nudos_feature_class, campos) as cursor:
        for row in cursor:
            id_punto = row[0]
            tiponudo = row[1]
            coordenadas = row[2]  # Esto devuelve una tupla (x, y)
            # Almacenar las coordenadas y matricula en el diccionario
            puntos_dict[id_punto] = {'Coordenadas': coordenadas, 'tiponudo': tiponudo}

    return puntos_dict

def actualizar_nudos_en_tramos(feature_class, vertices_tramos, info_puntos_cctt, info_nudos):
    campos = ['id', 'SHAPE@', 'nudoorigen', 'nudofin', 'idcd', 'tension', 'propiedad', 'longitud']

    with arcpy.da.UpdateCursor(feature_class, campos) as cursor:
        for row in cursor:
            id_tramo = generar_id_unico()  # Generar un ID único para cada tramo
            geometria_tramo = row[1]
            inicio_tramo = (geometria_tramo.firstPoint.X, geometria_tramo.firstPoint.Y)
            fin_tramo = (geometria_tramo.lastPoint.X, geometria_tramo.lastPoint.Y)

            # Calcular la longitud del tramo
            longitud_tramo = calcular_longitud_linea(inicio_tramo, fin_tramo)

            nudoorigen_actualizado = None
            nudofin_actualizado = None

            for id_cctt, info in info_puntos_cctt.items():
                if inicio_tramo == info['Coordenadas']:
                    nudoorigen_actualizado = id_cctt
                if fin_tramo == info['Coordenadas']:
                    nudofin_actualizado = id_cctt

            if not nudoorigen_actualizado or not nudofin_actualizado:
                for id_nudo, info in info_nudos.items():
                    if inicio_tramo == info['Coordenadas'] and not nudoorigen_actualizado:
                        nudoorigen_actualizado = id_nudo
                    if fin_tramo == info['Coordenadas'] and not nudofin_actualizado:
                        nudofin_actualizado = id_nudo

            if nudoorigen_actualizado or nudofin_actualizado:
                row[0] = id_tramo  # Asignar el nuevo ID único
                if nudoorigen_actualizado:
                    row[2] = nudoorigen_actualizado
                    row[4] = nudoorigen_actualizado
                    row[5] = 400
                    row[6] = 1
                if nudofin_actualizado:
                    row[3] = nudofin_actualizado
                row[7] = longitud_tramo  # Asignar la longitud calculada
                cursor.updateRow(row)

def determinar_tipo_tramo(tipo_inicio, tipo_fin):
    tipo_tramo_rules = {
        ('ap', 'ap'): 't',
        ('ap', 'ag'): 't',
        ('ap', 'aq'): 'p',
        ('ag', 'ap'): 't',
        ('ag', 'ag'): 'p',
        ('ag', 'aq'): 'p',
        ('aq', 'ag'): 'p',
        ('aq', 'ap'): 'p',
        ('aq', 'aq'): 's',
    }
    return tipo_tramo_rules.get((tipo_inicio, tipo_fin), None)

def actualizar_tipos_tramos(feature_class, info_puntos_cctt, info_nudos):
    campos = ['id', 'SHAPE@', 'nudoorigen', 'nudofin', 'tipo']  # Asumiendo que el campo tipo existe para almacenar el tipo de tramo

    with arcpy.da.UpdateCursor(feature_class, campos) as cursor:
        for row in cursor:
            geometria_tramo = row[1]
            inicio_tramo = (geometria_tramo.firstPoint.X, geometria_tramo.firstPoint.Y)
            fin_tramo = (geometria_tramo.lastPoint.X, geometria_tramo.lastPoint.Y)

            # Determinar el tipo de nudo para inicio y fin
            tipo_inicio = obtener_tipo_nudo(inicio_tramo, info_puntos_cctt, info_nudos)
            tipo_fin = obtener_tipo_nudo(fin_tramo, info_puntos_cctt, info_nudos)

            # Determinar el tipo de tramo basado en los tipos de nudos de inicio y fin
            tipo_tramo = determinar_tipo_tramo(tipo_inicio, tipo_fin)
            if tipo_tramo:
                row[4] = tipo_tramo  # Actualizar el tipo de tramo
                cursor.updateRow(row)

def obtener_tipo_nudo(coordenadas, info_puntos_cctt, info_nudos):
    for id_nudo, info in info_nudos.items():
        if coordenadas == info['Coordenadas']:
            return info['tiponudo']
    for id_cctt, info in info_puntos_cctt.items():
        if coordenadas == info['Coordenadas']:
            return 'ag'  # Asumir tipo 'ag' para cctt
    return None




def recorrer_y_procesar(base_dir):
    for root, dirs, files in os.walk(base_dir):
        shp_files = glob.glob(os.path.join(root, "*.shp"))
        cctt_files = [f for f in shp_files if "cctt" in os.path.basename(f)]
        nudos_files = [f for f in shp_files if "nudos" in os.path.basename(f)]
        tramos_files = [f for f in shp_files if "tramos_final" in os.path.basename(f)]

        # Asegurarse de que haya exactamente un archivo de cada tipo antes de proceder
        if len(cctt_files) == 1 and len(nudos_files) == 1 and len(tramos_files) == 1:
            cctt_file = cctt_files[0]
            nudos_file = nudos_files[0]
            tramos_file = tramos_files[0]

            print(f"Procesando: CCTT={os.path.basename(cctt_file)}, Nudos={os.path.basename(nudos_file)}, Tramos={os.path.basename(tramos_file)}")

            # Aquí llamas a tus funciones con los paths completos de los archivos encontrados
            listar_campos_y_tipos(tramos_file)
            actualizar_campos(tramos_file)
            vertices_tramos = obtener_vertices_tramos(tramos_file)
            info_puntos_cctt = obtener_info_puntos_cctt(cctt_file)
            info_nudos = obtener_info_nudos(nudos_file)
            actualizar_nudos_en_tramos(tramos_file, vertices_tramos, info_puntos_cctt, info_nudos)
            actualizar_tipos_tramos(tramos_file, info_puntos_cctt, info_nudos)
        else:
            print(f"Advertencia: No se encontraron los archivos necesarios en {root}")

if __name__ == "__main__":
    base_dir = config.BASE_DIR
    recorrer_y_procesar(base_dir)
