import rdflib
import geopandas as gpd
from shapely.geometry import Point, Polygon

# 1. Extraer los datos del archivo Turtle
g = rdflib.Graph()
g.parse(r"D:\Minsait_Curro\Recursos_Por\Vegetacion\COS.shp.ttl", format="turtle")

# 2. Convertir los datos a geometrías de Shapely
# Suponiendo que las coordenadas del polígono están en una propiedad específica, ajusta la consulta SPARQL según sea necesario
qres = g.query(
    """
    PREFIX spo: <http://crossforest.eu/position/ontology/>
    SELECT ?polygon
    WHERE {
        ?polygon a spo:Polygon .
    }
    """
)

polygons = []
for row in qres:
    # Asume que los puntos del polígono están separados por comas y las coordenadas por espacios
    coords = [tuple(map(float, coord.split())) for coord in str(row[0]).split(',')]
    polygons.append(Polygon(coords))

# 3. Crear un GeoDataFrame con Geopandas
gdf = gpd.GeoDataFrame(geometry=polygons)

# 4. Exportar el GeoDataFrame a un archivo Shapefile
gdf.to_file("LandUse.shp")

