import json
import os
import config
import uuid


def cargar_json(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        return json.load(archivo)

def guardar_json(datos, ruta_archivo):
    with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)

def asegurar_claves_como_str(tramos):
    """Asegura que las claves 'nudoorigen' y 'nudofin' en todos los tramos sean strings."""
    errores = {'nudoorigen': [], 'nudofin': []}
    for tramo in tramos:
        # Verificar y corregir 'nudoorigen'
        if 'nudoorigen' in tramo and not isinstance(tramo['nudoorigen'], str):
            errores['nudoorigen'].append(tramo['id'])
            tramo['nudoorigen'] = str(tramo['nudoorigen'])
        # Verificar y corregir 'nudofin'
        if 'nudofin' in tramo and not isinstance(tramo['nudofin'], str):
            errores['nudofin'].append(tramo['id'])
            tramo['nudofin'] = str(tramo['nudofin'])
        # Asegurar que el 'id' sea un string
        tramo['id'] = str(tramo['id'])
    return errores



def insertar_actualizaciones(original, modificado):
    total_correcciones = 0
    for cctt_modificado in modificado['cctt']:
        idcd_modificado_str = str(cctt_modificado['idcd'])
        cctt_original = next((item for item in original['cctt'] if str(item['idcd']) == idcd_modificado_str), None)
        if cctt_original:
            if cctt_original.get('nudos') and isinstance(cctt_original['nudos'], list) and cctt_original['nudos']:
                primer_nudo = cctt_original['nudos'][0]
                primer_nudo['id'] = str(primer_nudo['id'])
                primer_nudo['tiponudo'] = 'ap'

                nuevo_nudo = {
                    'id': str(uuid.uuid4()),  # Usar uuid para generar un ID único
                    'tiponudo': 'ct',
                    'x': cctt_original['x'],
                    'y': cctt_original['y']
                }
                for key in primer_nudo:
                    if key not in ['x', 'y', 'tiponudo', 'id']:
                        nuevo_nudo[key] = primer_nudo[key]
                cctt_original['nudos'].insert(0, nuevo_nudo)
            tramos_para_insertar = cctt_original.get('tramos', [])
        for tramo_modificado in cctt_modificado.get('tramos', []):
            asegurar_claves_como_str([tramo_modificado])
            if tramo_modificado not in tramos_para_insertar:
                tramos_para_insertar.append(tramo_modificado)
            cctt_original['tramos'] = tramos_para_insertar

    return original


def procesar_archivos_masivamente(ruta_originales, ruta_modificados, ruta_actualizados):
    os.makedirs(ruta_actualizados, exist_ok=True)

    originales_map = {nombre.replace('_processed', ''): nombre for nombre in os.listdir(ruta_originales)}

    for nombre_archivo_modificado in os.listdir(ruta_modificados):
        nombre_archivo_original = originales_map.get(nombre_archivo_modificado, None)

        if nombre_archivo_original:
            ruta_origen = os.path.join(ruta_originales, nombre_archivo_original)
            ruta_modificado = os.path.join(ruta_modificados, nombre_archivo_modificado)
            ruta_salida = os.path.join(ruta_actualizados, nombre_archivo_modificado)

            contenido_original = cargar_json(ruta_origen)
            contenido_modificado = cargar_json(ruta_modificado)
            contenido_actualizado = insertar_actualizaciones(contenido_original, contenido_modificado)

            errores = asegurar_claves_como_str(contenido_actualizado['cctt'][0]['tramos'])  # Asume que siempre hay al menos un CCTT y que los tramos están presentes

            if errores['nudoorigen'] or errores['nudofin']:
                print(f"Corregidos nudoorigen y/o nudofin en {nombre_archivo_modificado}: {errores}")

            guardar_json(contenido_actualizado, ruta_salida)
            print(f'Archivo actualizado guardado: {ruta_salida}')
        else:
            print(f'No se encontró archivo original correspondiente para: {nombre_archivo_modificado}')

if __name__ == "__main__":
    ruta_originales = config.JSON_USADOS_DIR
    ruta_modificados = config.JSON_SALIDAS_DIR
    ruta_actualizados = config.ACTUALIZADOS_DIR

    if not os.path.exists(ruta_actualizados):
        os.makedirs(ruta_actualizados)

    procesar_archivos_masivamente(ruta_originales, ruta_modificados, ruta_actualizados)
