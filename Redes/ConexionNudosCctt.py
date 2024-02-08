import os
import glob
import geopandas as gpd
import networkx as nx
from shapely.geometry import LineString
import pandas as pd
import arcpy
import config

def recorrer_y_procesar(base_dir):
    for root, dirs, files in os.walk(base_dir):
        shp_files = glob.glob(os.path.join(root, "*.shp"))
        cctt_files = [f for f in shp_files if "cctt" in f]
        nudos_files = [f for f in shp_files if "nudos" in f]
        tramos_files = [f for f in shp_files if "tramos" in f]

        for cctt_file, nudos_file, tramos_file in zip(cctt_files, nudos_files, tramos_files):
            procesar_archivos_shp(cctt_file, nudos_file, tramos_file)

def calcular_distancia_y_nudo_mas_cercano(cctt, unidad, gdf_nudos, tipo_nudos_permitidos=['aq', 'ap', 'ag'], radio=200):
    nudos_unidad = gdf_nudos[gdf_nudos['id'].isin(unidad) & gdf_nudos['tiponudo'].isin(tipo_nudos_permitidos)]
    if nudos_unidad.empty:
        return None, None

    distancias = nudos_unidad.geometry.distance(cctt.geometry)
    nudo_cercano_idx = distancias.idxmin()
    distancia_min = distancias.min()

    if distancia_min <= radio:
        return nudos_unidad.loc[nudo_cercano_idx], distancia_min
    return None, None

def actualizar_tiponudo_a_ap(nudos_file):
    with arcpy.da.UpdateCursor(nudos_file, "tiponudo") as cursor:
        for row in cursor:
            if row[0] == "ct":
                row[0] = "ap"
                cursor.updateRow(row)

def agregar_nuevos_tramos_a_shp(tramos_file, nuevos_tramos):
    campos = arcpy.ListFields(tramos_file)
    tipos_campos = {campo.name: campo.type for campo in campos if campo.name != 'OBJECTID' and campo.type != 'Geometry'}
    nombres_campos = [campo.name for campo in campos if campo.name != 'OBJECTID' and campo.type != 'Geometry']
    nombres_campos.insert(0, "SHAPE@")

    with arcpy.da.InsertCursor(tramos_file, nombres_campos) as cursor:
        for tramo in nuevos_tramos:
            row = []
            for nombre_campo in nombres_campos:
                if nombre_campo == "SHAPE@":
                    row.append(tramo['geometry'])
                elif nombre_campo == "idcd":  # Asegúrate de que el nombre del campo sea el correcto
                    row.append(tramo['idcd'])
                else:
                    valor = tramo.get(nombre_campo, None)
                    tipo_campo = tipos_campos[nombre_campo]
                    if tipo_campo in ['Double', 'Float', 'Single']:
                        row.append(float(valor))
                    elif tipo_campo in ['Integer', 'SmallInteger']:
                        row.append(int(valor))
                    elif tipo_campo == 'String':
                        row.append(str(valor))
                    else:
                        row.append(valor)
            cursor.insertRow(row)

def procesar_archivos_shp(cctt_file, nudos_file, tramos_file):
    actualizar_tiponudo_a_ap(nudos_file)

    gdf_cctt = gpd.read_file(cctt_file)
    gdf_nudos = gpd.read_file(nudos_file)
    gdf_tramos = gpd.read_file(tramos_file)

    # Obtener lista de campos (nombres y tipos) de la capa tramos
    campos_tramos = [(e.name, e.type) for e in arcpy.ListFields(tramos_file)]

    G = nx.Graph()
    for _, tramo in gdf_tramos.iterrows():
        G.add_edge(tramo['nudoorigen'], tramo['nudofin'], weight=1)

    componentes = list(nx.connected_components(G))

    nuevos_tramos = []
    conexion_registros = []

    for cctt in gdf_cctt.itertuples():
        for unidad in componentes:
            nudo_cercano, distancia = calcular_distancia_y_nudo_mas_cercano(cctt, unidad, gdf_nudos, radio=200)
            if nudo_cercano is not None:
                # Preparar un diccionario para el nuevo tramo, inicialmente solo con geometría e 'idcd'
                nuevo_tramo = {'geometry': LineString([cctt.geometry, nudo_cercano.geometry]), 'idcd': cctt.idcd}

                # Heredar los atributos de los tramos existentes, ajustando por nombre y tipo
                for campo, tipo in campos_tramos:
                    if campo.lower() in ['geometry', 'shape']:  # Excluir campo de geometría
                        continue
                    # Asignar un valor por defecto basado en el tipo de campo
                    if tipo == 'String':
                        nuevo_tramo[campo] = ''
                    elif tipo in ['Double', 'Integer', 'Float', 'Short']:
                        nuevo_tramo[campo] = 0
                    # Agregar lógica adicional si hay otros tipos de datos

                nuevos_tramos.append(nuevo_tramo)
                conexion_registros.append(f"CCTT {cctt.idcd} conectado a nudo {nudo_cercano.id} dentro de {distancia:.2f}m.")

    # Convertir la lista de nuevos tramos a un GeoDataFrame
    gdf_nuevos_tramos = gpd.GeoDataFrame(nuevos_tramos, geometry='geometry', crs=gdf_cctt.crs)

    # Guardar solo los nuevos tramos en el archivo "_final.shp"
    output_file = os.path.splitext(tramos_file)[0] + "_final.shp"
    gdf_nuevos_tramos.to_file(output_file)

    print(f"Se intentó conectar {len(gdf_cctt)} CCTTs.")
    print(f"Se establecieron {len(nuevos_tramos)} nuevas conexiones.")
    for registro in conexion_registros:
        print(registro)


if __name__ == "__main__":
    base_dir = config.BASE_DIR
    recorrer_y_procesar(base_dir)
