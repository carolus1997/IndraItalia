"""
    Fichero que contiene las funciones necesarias para obtener datos de OSM a través de osmnx
"""

# Importamos librerias necesarias
import osmnx as ox
import geopandas as gpd
from pyproj import Transformer


class DescargaOSm:

    @staticmethod
    def descargar_geometrias_por_poligono(poligono, etiquetas):
        """
            Descarga geometrias a partir de un poligono y las devuelve en un Geodataframe

            :param poligono: Poligono de solicitud
            :type poligono: Polygon

            :param etiquetas: Diccionario con las etiquetas para las condiciones de descarga
            :type etiquetas: dict

            :return: Geodataframe resultante de la descarga
            :rtype: Geodataframe
        """

        gdf = ox.geometries_from_polygon(poligono, etiquetas)
        return gdf

    @staticmethod
    def descarga_grafo_por_poligono(poligono, *kwargs):
        """
            Descarga grafo de vias contenido por el poligono

            :param poligono: Poligono de solicitud
            :type poligono: Polygon

            :param kwargs: Parametros opcionales
            :type kwargs: tuple

            :return: Grafo obtenido, nodos y vias
            :rtype: Geodataframe, Geodataframe, Multidigraph

        """

        try:

            if len(kwargs) > 0:
                gdf = ox.graph_from_polygon(poligono, kwargs)
            else:
                gdf = ox.graph_from_polygon(poligono)

            gdf_nodos, gdf_edges = ox.graph_to_gdfs(gdf)

            return gdf_nodos, gdf_edges, gdf

        except:

            return gpd.GeoDataFrame(), gpd.GeoDataFrame(), gpd.GeoDataFrame()

    @staticmethod
    def descargar_geometrias_coordenadas(coordenadas: tuple, crs: int, etiquetas: dict, dist=1000):
        """
            Descarga las geometrias en base a unas coordenadas dadas

            :param coordenadas: Coordenadas en base a las que obtener la geometria
            :type coordenadas: tuple

            :param crs: Crs de las coordenadas dadas
            :type crs: int

            :param etiquetas: Diccionario con las etiquetas necesarias
            :type etiquetas: dict

            :param dist: Distanciaen metros en la que obtener las geometrias.
            :type dist: int

            :return: Geodataframe obtenido
            :rtype: Geodataframe

        """

        # Transformamos las coordenadas a 4326 para obtener los datos de OSM
        transformer = Transformer.from_crs(crs, 4326)
        puntos = transformer.transform(coordenadas[0], coordenadas[1])

        gdf = ox.geometries_from_point(puntos, etiquetas, dist)
        return gdf

    @staticmethod
    def descargar_grafo_por_coordenadas(coordenadas: tuple, crs: int, dist=1000, *kwargs):
        """
            Descarga el grafo de vias en base a las coordenadas dadas

            :param coordenadas: Coordenadas en base a las que obtener la geometria
            :type coordenadas: tuple

            :param crs: Crs de las coordenadas dadas
            :type crs: int

            :param dist: Distancia en las que obtener las geometrias
            :type dist: int

            :param kwargs: Parámetros opcionales
            :type kwargs: tuple

            :return: Geodataframe obtenido
            :rtype: Geodataframe

        """

        # Transformamos las coordenadas a 4326 para obtener los datos de OSM
        transformer = Transformer.from_crs(crs, 4326)
        puntos = transformer.transform(coordenadas[0], coordenadas[1])

        if len(kwargs) > 0:
            gdf = ox.graph_from_point(puntos, dist, kwargs)
        else:
            gdf = ox.graph_from_point(puntos, dist)

        gdf_nodos, gdf_edges = ox.graph_to_gdfs(gdf)

        return gdf_nodos, gdf_edges, gdf
