import geopandas as gpd
import networkx as nx
import momepy
from shapely.geometry import Point

callejero = input('Introduce la ruta de la capa de carreteras y calles: ')
coord1 = input('Introduce las coordenadas del punto de inicio (Ej: 38.339366,-0.4907572): ')
coord2 = input('Introduce las coordenadas del punto de destino (Ej: 38.339366,-0.4907572): ')
# Lectura de la capa de calles
calles = gpd.read_file(callejero)

# Dividir geometrías multipartitas en geometrías simples
calles_exploded = calles.explode(index_parts=True).reset_index(drop=True)

# Diccionario para la jerarquía de las carreteras
carreteras_dict = {
    "unclassified": (0, "track"),
    "proposed": (0, "track"),
    "platform": (0, "track"),
    "path": (1, "track"),
    "road": (1, "track"),
    "service": (1, "track"),
    "track": (1, "residential"),
    "track_grade1": (1, "residential"),
    "track_grade2": (1, "residential"),
    "track_grade3": (1, "residential"),
    "track_grade4": (1, "residential"),
    "track_grade5": (1, "residential"),
    "cycleway": (2, "residential"),
    "footway": (2, "residential"),
    "step": (2, "residential"),
    "pedestrian": (2, "residential"),
    "living_street": (2, "residential"),
    "bridleway": (2, "residential"),
    "residential": (2, "residential"),
    "primary_link": (3, "primary"),
    "primary": (3, "primary"),
    "rest_area": (4, "secondary"),
    "secondary_link": (4, "secondary"),
    "secondary": (4, "secondary"),
    "tertiary_link": (5, "tertiary"),
    "tertiary": (5, "tertiary"),
    "trunk": (6, "motorway"),
    "trunk_link": (6, "motorway"),
    "services": (6, "motorway"),
    "motorway_link": (6, "motorway"),
    "motorway": (6, "motorway")
}

# Aplica la jerarquía de las carreteras al dataframe
calles_exploded['Codigo'] = calles_exploded['fclass'].map(lambda x: carreteras_dict.get(x, (None, None))[0])

# Conversión de geodataframe a grafo
G = momepy.gdf_to_nx(calles_exploded)

def nearest_node(gdf, x, y):
    """Función para encontrar el nodo más cercano a una coordenada dada."""
    point = Point(x, y)
    distances = gdf.geometry.distance(point)
    closest_index = distances.idxmin()
    return gdf.iloc[closest_index].name  # devuelve el índice del nodo más cercano

# Integración de la jerarquía de calles al grafo
for calle in calles.itertuples():
    # Usamos el campo "Codigo" para determinar el peso
    peso = 1 / calle.Codigo if calle.Codigo else float('inf')  # Si el código es None, el peso es infinito (evita ese camino)
    G[calle.source][calle.target]['weight'] = peso

# Usar la función nearest_node para obtener los nodos más cercanos
x1, y1 = coord1  # define tus coordenadas para el punto de inicio
x2, y2 = coord2  # define tus coordenadas para el punto final
nodo_inicio = nearest_node(calles, x1, y1)
nodo_final = nearest_node(calles, x2, y2)

ruta = nx.shortest_path(G, source=nodo_inicio, target=nodo_final, weight='weight')
print(ruta)
