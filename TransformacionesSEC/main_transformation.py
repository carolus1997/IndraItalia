"""
    Fichero principal para iniciar el script de transformación de capas de OSM
"""

# Importamos librerias
import argparse
import os
import sys
from datetime import datetime
from time import time

# Importamos ficheros locales
from script_transformacion_capas import TransformacionCapas

# Indicamos el directorio donde se encuentran los ficheros de entrada y la dirección de destino
directorio_entrada = "Santagata_cft"


directorio_destino = os.getcwd()+'/prueba_coord'


# Añadimos posibles argumentos que puede recibir el script, dandoles valor por defecto
parser = argparse.ArgumentParser()
parser.add_argument('-dc', '--entrada', nargs='?', default=directorio_entrada,
                    help='Indique directorio origen')


parser.add_argument('-dd', '--destino', nargs='?', default=directorio_destino,
                    help='Indique directorio origen')

# Opción de elementos entrada: poligono = shp con poligono base, coordenadas = coord (necesario tb crs_salida),
# zona = directorio shp osm
parser.add_argument('-op', '--opcion', nargs='?', default='poligono',
                    help='Indique opción: poligono, zonas, coordenadas')

# Si la opcion es tipo coordenadas necesario
parser.add_argument('-coord', '--coordenadas', nargs='?', default=(-436720.193,4503886.407),
                    help='Indique coordenadas')

# Si la opción es tipo coordenadas es necesario
parser.add_argument('-crs_coord', '--crs_coord', nargs='?', default=3857,
                   help='Indique crs al que pertenecen las coordenadas. Ej: 4326')

# Crs salida
parser.add_argument('-crs', '--crs', nargs='?', default=4326,
                    help='Indique crs: Ej: 25830')

# Leemos los argumentos recibidos
args = parser.parse_args()

# Comprobamos que estén los valores necesarios para iniciar la transformacion, si no, salimos del script

if not args.opcion:
    print("Se debe indicar opción de ejecución")
    sys.exit(1)

elif args.opcion != 'coordenadas' and not args.entrada:
    print("No se ha indicado directorio.")
    sys.exit(1)

elif not args.destino:
    print("No se indicó directorio de destino")
    sys.exit(1)

if args.opcion == 'coordenadas':
    if not args.coordenadas:
        print("Se deben indicar las coordenadas")
        sys.exit(1)
    if not args.crs_coord:
        print("El sistema de referencia origen es necesario")
        sys.exit(1)


if args.opcion == 'coordenadas' or args.opcion == "poligono":
    if not args.crs:
        print("Se debe indicar crs")
        sys.exit(1)


# Guardamos valores de los argumentos recibidos
directorio_entrada = args.entrada
directorio_destino = args.destino
opcion = args.opcion
coordenadas = args.coordenadas
crs = args.crs
crs_origen = args.crs_coord


# Iniciamos clase para transformación pasándole los paráemtros de los directorios de origen y destino
# y llamamos a función para iniciarla.
startTime = time()
print("Comienzo transformación, este proceso puede tardar  %s" % datetime.now().strftime('%d-%m-%Y %H:%M:%S'))

# Inicializamos la clase pasándole los parámetros necesarios y llamamos a la función de inicio de la misma
script_transformacion = TransformacionCapas(directorio_entrada, directorio_destino, crs)

# Vamos al inicio según opción seleccionada
if opcion == 'coordenadas':
    script_transformacion.iniciar_descarga_coordenadas_osm(coordenadas, crs_origen)
elif opcion == 'poligono':
    script_transformacion.iniciar_descarga_poligono_osm()
elif opcion == 'zonas':
    script_transformacion.iniciar_transformacion_zonas_osm()
else:
    print("Opcion seleccionada no válida")
    sys.exit(1)

# Indicamos final del proceso
print("Proceso finalizado  %s" %datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
elapsedTime = time() - startTime
print("Finalizado. Tiempo transcurrido: " + str(elapsedTime) + " segundos")


#   SCRIPT DE DESCARGA DE OSM EN BASE A COORDENADAS, POLIGONO O TRANSFORMACIÓN DE UNA ZONA COMPLETA
# TODO AÑADIR OPCION DE EN LA TRANSFORMACIÓN ZONA SEA SOLO DE UN MUNICIPIO
# TODO CREAR LOG
# TODO AÑADIR OPCION DE DESCARGA POR NOMBRE (PROVINCIA, PAIS, MUNICIPIO...)
