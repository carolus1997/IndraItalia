import geopandas as gpd
from osgeo import gdal
import networkx as nx
import momepy

calles = gpd.read_file('ruta_del_callejero.shp')
dataset = gdal.Open('ruta_del_raster.tif')
band = dataset.GetRasterBand(1)
array = band.ReadAsArray()



G = momepy.gdf_to_nx(calles)

transform = dataset.GetGeoTransform()

def get_raster_value(x, y, transform, array):
    col, row = int((x - transform[0]) / transform[1]), int((y - transform[3]) / transform[5])
    if 0 <= col < array.shape[1] and 0 <= row < array.shape[0]:
        return array[row][col]
    else:
        return None

for calle in calles.itertuples():
    valor_raster_inicio = get_raster_value(calle.geometry.coords[0][0], calle.geometry.coords[0][1], transform, array)
    valor_raster_final = get_raster_value(calle.geometry.coords[-1][0], calle.geometry.coords[-1][1], transform, array)

    if valor_raster_inicio and valor_raster_inicio > 0 and valor_raster_final and valor_raster_final > 0:
        # Ajusta el peso basado en la jerarquía de la calle.
        # Podrías invertir la jerarquía (por ej. 1/valor) para que calles de mayor jerarquía tengan menor costo.
        peso = 1 / calle.jerarquia

        # Agregar el peso al grafo
        G[calle.source][calle.target]['weight'] = peso

# Dado un nodo de inicio y uno final
nodo_inicio = (x1, y1)  # Debes definir estos valores
nodo_final = (x2, y2)  # Debes definir estos valores

ruta = nx.shortest_path(G, source=nodo_inicio, target=nodo_final, weight='weight')
print(ruta)
