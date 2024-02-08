"""
    Fichero que contiene las funciones y procesos necesarios para tratar las capas de OSM.

    Contiene la clase Transformacion Capas que al iniciar recibe la ruta donde se encuentran
    las capas de descarga, la ruta para las transformadas y el diccionario para filtrar los nombres
    de las capas que necesitamos (edificios, parcelas..)
"""

# Importaciones libraries necesarias
import glob
import os
from datetime import datetime
import geopandas as gpd
import configparser

# Importamos clases locales
from descarga_osm import DescargaOSm


class TransformacionCapas:
    """
        Clase que contiene los metodos necesarios para realizar la transformación de las capas
        descargadas de OSM.
    """
    def __init__(self, directorio_capas, directorio_destino, crs_salida):

        # Guardamos en la clase los datos de directorio
        self.directorio_entrada = directorio_capas
        self.directorio_destino = directorio_destino
        self.directorio_ficheros_salida = directorio_destino

        # Creamos lista de usos considerados como urbanos
        self.usos_urbanos = ['residential', 'industrial', 'comercial', 'retail', 'park', 'military', 'grass']

        # Iniciamos la ref_catastral
        self.ref_cat_actual = 1111111111111
        self.crs_salida = crs_salida

        self.config = configparser.ConfigParser()
        self.config.read("husos.conf")

        # DESCARGA Y TRANSFORMACION OSM (POLIGONO)
    def iniciar_descarga_poligono_osm(self):
        """
            Comprueba el directorio de origen e inicia la descarga a partir del poligono
            :return: None
        """

        if len(str(self.crs_salida)) == 2:
            self.crs_salida = int(self.config['husos'][str(self.crs_salida)])

        # Leemos el directorio de entrada
        dir_fentrada = os.listdir(self.directorio_entrada)

        # Si el primer elemento es un directorio iremos recorriendo los directorios que contiene
        if os.path.isdir(self.directorio_entrada + '/' + dir_fentrada[0]):
            for dir_ficheros in dir_fentrada:

                # Buscamos shp en los directoiros
                dir_shp = r'%s/*.shp' % (self.directorio_entrada + '/' + dir_ficheros + '/')
                ficheros = glob.glob(dir_shp)
                self.directorio_ficheros_salida = self.directorio_destino + '/' + dir_ficheros + '/'

                # Recorremos los shp para obtener los datos de OSM
                for fichero in ficheros:
                    self.obtener_datos_poligono_osm(fichero)

        # Si el primer elemento es un fichero recorremos el contenido del mismo para obtener los datos OSM
        elif os.path.isfile(self.directorio_entrada + '/' + dir_fentrada[0]):
            dir_shp = r'%s/*.shp' % self.directorio_entrada
            ficheros = glob.glob(dir_shp)

            for fichero in ficheros:
                nombre = os.path.splitext(os.path.basename(fichero))[0]
                self.directorio_ficheros_salida = self.directorio_destino + '/' + nombre
                self.obtener_datos_poligono_osm(fichero)

    def obtener_datos_poligono_osm(self, fichero):
        """
            Iniciamos el proceso para obtener las capas OSM en función a un poligono guardado en shp.

            :param fichero: ruta del fichero shp que contiene el polígono
            :type fichero: str

            :return: None
        """

        # Reseteamso la ref_catastral
        self.ref_cat_actual = 1111111111111

        # Si no existe el directorio para los ficheros de salida lo creamos
        if not os.path.isdir(self.directorio_ficheros_salida):
            os.makedirs(self.directorio_ficheros_salida)

        # Leemos el fichero y obtenemos polygono del geodataframe
        capa = gpd.read_file(fichero)

        if capa.empty:
            print('El elemento no contiene geometria')
            return False

        # Guardamos el crs_salida de origen y lo convertimos a 4326 para obtener los datos de OSM
        # crs_salida = capa.crs_salida
        cft = capa.dissolve()
        capa = cft
        if str(cft.crs) != "epsg:4326":
            capa['geometry'] = capa.geometry.to_crs("epsg:4326")

        poligono = capa.iloc[0]['geometry']

        # Obtenemos geodataframes de edificios, usos y vias
        print("Descargando edificios")
        gdf_edificios = DescargaOSm.descargar_geometrias_por_poligono(poligono, {'building': True})

        print("Descargando parcelas")
        gdf_usos = DescargaOSm.descargar_geometrias_por_poligono(poligono, {'landuse': True})

        print("Descargando vias")
        gdf_nodos, gdf_vias, gdf = DescargaOSm.descarga_grafo_por_poligono(poligono)

        # poligono = gpd.GeoDataFrame(poligono)

        try:
            self.tratar_capas_osm_descargadas(gdf_usos, gdf_edificios, gdf_vias, cft)

        except Exception as e:
            f = open("Erroneos_%s.txt" % os.path.basename(self.directorio_destino), "a")
            f.write("\n %s" % os.path.basename(self.directorio_ficheros_salida))
            f.close()
            print(e, str(fichero))

    # DESCARGA Y TRANSFORMACION OSM (COORDENADAS)
    def iniciar_descarga_coordenadas_osm(self, coordenadas, crs_origen):
        """
            Descarga los Geodataframe a través de las coordenadas recibidas e inicia la transformacion de los mismos

            :param coordenadas: Coordenadas de las que obtener las capas
            :type coordenadas: tuple

            :param crs: CRS en las que están las coordenadas
            :type crs: int

            :return: None
        """

        self.ref_cat_actual = 1111111111111

        # Obtenemos geodataframes de edificios, usos y vias
        gdf_edificios = DescargaOSm.descargar_geometrias_coordenadas(coordenadas, crs_origen, {'building': True})
        gdf_usos = DescargaOSm.descargar_geometrias_coordenadas(coordenadas, crs_origen, {'landuse': True})
        gdf_nodos_vias, gdf_vias, gdf = DescargaOSm.descargar_grafo_por_coordenadas(coordenadas, crs_origen)

        # Llamamos a función encargada de iniciar la transformación de las capas
        self.tratar_capas_osm_descargadas(gdf_usos, gdf_edificios, gdf_vias)

    # TRANSFORMAR ZONAS DESCARGADS OSM (GEOFABRIK)
    def iniciar_transformacion_zonas_osm(self):

        dir_capas = os.listdir(self.directorio_entrada)

        if os.path.isdir(self.directorio_entrada + '/' + dir_capas[0]):
            # Recorremos los directorios de la carpeta de origen
            for zona in os.listdir(self.directorio_entrada):

                nombre_zona = zona.split('.')[0]
                self.directorio_destino = self.directorio_ficheros_salida + '/' + nombre_zona
                if not os.path.isdir(self.directorio_destino):
                    os.makedirs(self.directorio_destino)
                self.transformar_zona(self.directorio_entrada + '/' + zona)

        elif os.path.isfile(self.directorio_entrada + '/' + dir_capas[0]):

            # Si solo se indica una zona
            nombre_zona = os.path.splitext(os.path.basename(self.directorio_entrada))[0]
            self.directorio_destino = self.directorio_ficheros_salida + '/' + nombre_zona

            if not os.path.isdir(self.directorio_destino):
                os.makedirs(self.directorio_destino)

            self.transformar_zona(self.directorio_entrada)

    def transformar_zona(self, dir_zona):
        """
            Inicia la lectura y transformación de las capas OSM de una zona

            :param dir_zona: Directorio donde se encuentran las capas de la zona
            :type dir_zona: str

            :return: None
        """

        # Creo dataframe para cargar la capa de zonas
        print('Leyendo capa de zona')
        zonas = gpd.read_file(dir_zona+'/gis_osm_places_a_free_1.shp')

        print("Leyendo capa vias")
        vias = gpd.read_file(dir_zona+'/gis_osm_roads_free_1.shp')

        print("Leyendo capa usos")
        usos = gpd.read_file(dir_zona+'/gis_osm_landuse_a_free_1.shp')

        print("Leyendo capa edificios")
        edificios = gpd.read_file(dir_zona+'/gis_osm_buildings_a_free_1.shp')

        # Obtengo los municipios mediante el campo locality de la capa places
        municipios = zonas[zonas.fclass == "locality"]
        # municipios = zonas[zonas.name == "Castelliere di Siena Vecchia"]

        # Recorremos los municipios para transformarlos
        for i in range(len(municipios)):

            try:
                municipio = municipios.iloc[[i]]

                nombre_municipio = municipio.iloc[0]['name']
                if nombre_municipio is None:
                    nombre_municipio = "Desconocido_%s" % municipio.iloc[0]['osm_id']

                self.directorio_ficheros_salida = self.directorio_destino + '/' + str(nombre_municipio)

                if not os.path.isdir(self.directorio_ficheros_salida):
                    os.makedirs(self.directorio_ficheros_salida)

            except Exception as e:
                print(str(e))

                continue

            if len(os.listdir(self.directorio_ficheros_salida)) > 0:
                continue

            print('Comienza transformación capas de %s - %s' % (nombre_municipio,
                                                                datetime.now().strftime('%d-%m-%Y %H:%M:%S')))

            self.transformar_municipio(municipio, vias, edificios, usos)

    def transformar_municipio(self, capa_municipio, capa_vias, capa_edificios, capa_parcelas):
        """
            Función para obtener las capas de un municipio

            :param capa_municipio: Geodataframe con los datos del municipio
            :type capa_municipio: Geodataframe

            :param capa_vias: Geodataframe con los datos de vias de la zona
            :type capa_vias: Geodataframe

            :param capa_edificios: Geodataframe con datos de edificios de la zona
            :type capa_edificios: Geodataframe

            :param capa_parcelas: Geodataframe con datos de parcelas de la zona
            :type capa_parcelas: Geodataframe

            :return: None
        """

        self.ref_cat_actual = 1111111111111

        # Obtenemos las parcelas que corresponden al municipio
        parcelas_municipio = gpd.sjoin(capa_parcelas, capa_municipio)
        parcelas_municipio.drop('index_right', axis=1, inplace=True)

        # Obtenemos parcelas clasificadas por su uso
        parcelas_usos = self.obtener_parcelas_usos(parcelas_municipio,  'fclass_left')

        # Obtenemos vias del municipio
        vias_municipio = gpd.sjoin(capa_vias, parcelas_municipio)

        # Si hay vias, eliminamos duplicados y guardamos vias
        if not vias_municipio.empty:
            vias_municipio.drop_duplicates(inplace=True)
            self.guardar_capas_sec(vias_municipio, 'vias')

        # Obtenemos las vias con la estructura SEC
        vias = self.obtener_vias_sec(vias_municipio, parcelas_usos, 'fclass')

        # Llamamos a función que creará las capas de parcelas y guardara el shp de rurales
        parcelas_municipio = self.crear_capas_parcelas(parcelas_usos, vias)

        self.guardar_capas_sec(parcelas_municipio, 'parcela_r_d')


        # Llamamos a función que obtiene y guarda los edificios (rurales y urbanos)
        self.crear_capas_edificios(parcelas_municipio, capa_edificios)

    # TRANSFORMACION Y GUARDADO COMUNES
    def tratar_capas_osm_descargadas(self, gdf_usos, gdf_edificios, gdf_vias,  cft=None):
        """
            Inicia la transformación de los geodataframe obtenidos a las capas

            :param gdf_usos: Geodataframe de las parcelas según su uso
            :type gdf_usos: Geodataframe

            :param gdf_edificios: Geodataframe de edificios
            :type gdf_edificios: Geodataframe

            :param gdf_vias: Geodataframe de vias
            :type gdf_vias: Geodataframe

            :return: None
        """

        print("Comienza transformación capas descargadas")

        # Transformamos los geodataframe al CRS de salida y nos quedamos con las geometrias correctas
        gdf_usos.to_crs(self.crs_salida, inplace=True)
        # gdf_usos = gdf_usos[gdf_usos.geometry.type == 'Polygon']

        gdf_edificios.to_crs(self.crs_salida, inplace=True)
        # gdf_edificios = gdf_edificios[gdf_edificios.geometry.type == 'Polygon']

        if not gdf_vias.empty:
            gdf_vias.to_crs(self.crs_salida, inplace=True)
            # gdf_vias = gdf_vias[gdf_vias.geometry.type == 'LineString']

        # Llamamos a función para obtener las parcelas

        if not cft is None:
            parcelas = self.obtener_parcelas_usos(gdf_usos, 'landuse',  cft)
        else:
            parcelas = self.obtener_parcelas_usos(gdf_usos, 'landuse')

        # Eliminamos duplicados y guardamos capa de vias
        gdf_vias.drop_duplicates(subset='geometry', inplace=True)

        vias_poligono = gdf_vias

        # Obtenemos las vias, parcelas y edificios
        if not gdf_vias.empty:

            vias_poligono = self.obtener_vias_sec(gdf_vias, parcelas, 'highway')

            # Guardamos capa vias
            # Modificamos los campos que sean lista a str para evitar errores al guardar el shp
            gdf_vias_nl = gdf_vias.applymap(lambda x: str(x) if isinstance(x, list) else x)
            gdf_vias_nl.set_geometry('geometry', inplace=True)
            gdf_vias_nl.set_crs(self.crs_salida, inplace=True, allow_override=True)
            gdf_vias_nl['geometry'] = gdf_vias.geometry.to_crs(self.crs_salida)

            self.guardar_capas_sec(gdf_vias_nl, 'vias')

        parcelas_usos = self.crear_capas_parcelas(parcelas, vias_poligono)

        self.guardar_capas_sec(parcelas_usos, 'parcela_r_d')

        self.crear_capas_edificios(parcelas_usos, gdf_edificios)

    def obtener_parcelas_usos(self, parcelas_municipio, key_uso, cft=None):
        """

            Clasifica las parcelas según sus usos y devuelve el resultado

            :param parcelas_municipio: Capa de parcelas del municipio
            :type parcelas_municipio: Geodataframe

            :param key_uso: Nombre de la columna en la que se guarda el uso
            :type key_uso: str

            :return: Capa de parcelas clasificada según uso
            :rtype: Geodataframe
        """

        print("Clasificación de parcelas según uso")

        # Creamos la capa con las columnas finales y la lista de las geometrias
        parcelas_usos = gpd.GeoDataFrame(columns=['USO', 'TIPOPOL', 'PROP', 'CONSTRU', 'REFCAT'])
        geometrias = []

        # Recorremos la capa parcelas
        for i in range(len(parcelas_municipio)):

            #  guardamos el poligono y la geometria del mismo y lo añadimos a la capa geometrias
            poligono = parcelas_municipio.iloc[i]
            geom = poligono['geometry']
            geometrias.append(geom)

            # Creamos referencia catastral aleatoria
            referencia_c = self.ref_cat_actual

            # Indicamos su uso
            if poligono[key_uso] in self.usos_urbanos:
                uso = 'URBANO'
            else:
                uso = 'RURAL'

            # Añadimos los datos a la nueva capa indicando su uso y completando resto de las columnas
            parcelas_usos = parcelas_usos.append({
                'USO': uso,
                'TIPOPOL': 'PARCELA',
                'PROP': 'PRIVADO',
                'CONSTRU': 'SUELO',
                'REFCAT': referencia_c,
            }, ignore_index=True)

        # Guardamos geometrias e indicamos el crs_salida y devolvemos el resultado
        parcelas_usos.geometry = geometrias
        parcelas_usos.set_crs(parcelas_municipio.crs, inplace=True)

        if cft is not None:
            if cft.crs != parcelas_usos.crs:
                cft.to_crs(parcelas_usos.crs, inplace=True)

            parcelas_huecos = gpd.overlay(cft, parcelas_usos, how="difference")

            parcelas_nuevas = gpd.GeoDataFrame()
            parcelas_nuevas['geometry'] = parcelas_huecos.geometry
            parcelas_nuevas = parcelas_nuevas.explode()

            parcelas_nuevas.set_geometry(col='geometry', inplace=True)
            parcelas_nuevas = parcelas_nuevas.loc[parcelas_nuevas['geometry'].is_valid, :]

            parcelas_nuevas['USO'] = parcelas_huecos.iloc[0]['density'].upper()
            parcelas_nuevas['PROP'] = 'INDETERMINADO'
            parcelas_nuevas['CONSTRU'] = 'SUELO'
            parcelas_nuevas['REFCAT'] = str(self.ref_cat_actual)
            parcelas_nuevas['TIPOPOL'] = 'PARCELA'

            parcelas_usos = parcelas_usos.append(parcelas_nuevas)

            parcelas_nuevas['PROP'] = parcelas_nuevas.apply(lambda row: 'PRIVADO' if row['geometry'].area <= 400
                                                            else 'INDETERMINADO', axis=1)



        return parcelas_usos

    def obtener_vias_sec(self, vias_mun, parcelas_municipio, key_via):

        """
            Obtenemos la capa de vias con las columnas finales

            :param vias_mun: Capo vias del municipio
            :type vias_mun: Geodataframe

            :param parcelas_municipio: Capa de parcelas del municipio
            :type parcelas_municipio: Geodataframe

            :param key_via: Nombre de la columna donde se indica tipo de via
            :param key_via: str

            :return: Capa vias
            :rtype: Geodataframe
        """

        print("Obtener vias poligonos")

        # Guardamos crs_salida original del geodataframe
        crs = vias_mun.crs

        # Transformamos gdf a un crs_salida en el que aplicar buffer en metros
        vias_mun = vias_mun.to_crs(3763)

        # Creamos lista geom y recorremos capa para aplicar buffer según tipo geom
        geometrias = []
        for num_elemento in range(len(vias_mun)):

            # Obtenemos tipo via
            tipo_via = str(vias_mun.iloc[num_elemento][key_via]).lower()

            # Aplicamos buffer según el tipo de via
            buffer = 5
            if 'motorway' in tipo_via:
                buffer = 19
            elif 'primary' in tipo_via:
                buffer = 12
            elif 'sencondary' in tipo_via:
                buffer = 9

            geom_buffer = vias_mun.loc[vias_mun.index[num_elemento], 'geometry'].buffer(buffer, cap_style=2)
            geometrias.append(geom_buffer)

        # Creamos geodataframe para las vias, aplicamos geometrias y reproyectamos a crs_salida original
        vias = gpd.GeoDataFrame(columns=['geometry', 'TIPOPOL', 'PROP', 'REFCAT'])

        vias.set_geometry(geometrias, inplace=True)
        vias.set_crs(3763, inplace=True)
        vias = vias.to_crs(crs)
        vias['geometry'] = vias.geometry.buffer(0)

        # Guardamos valores tipopol y propiedad
        vias['TIPOPOL'] = "VIA"
        vias['PROP'] = "PUBLICO"

        # Obtenemos capa vias del municipio y creamos geodataframe para vias del mismo
        vias_usos = gpd.sjoin(vias, parcelas_municipio)
        vias_sec = gpd.GeoDataFrame(columns=['geometry', 'TIPOPOL', 'PROP', 'REFCAT', 'USO', 'CONSTRU'])

        # Recorremos la capa vias obtenida para crear la capa vias con los campos correspondientes
        for i in range(len(vias_usos)):
            poligono = vias_usos.iloc[i]
            referencia_c = self.ref_cat_actual

            vias_sec = vias_sec.append({
                'USO': poligono['USO'],
                'TIPOPOL': poligono['TIPOPOL_left'],
                'PROP': poligono['PROP_left'],
                'CONSTRU': 'CAMINO',
                'REFCAT': referencia_c,
                'geometry': poligono['geometry']
            }, ignore_index=True)

        vias_sec.set_crs(crs, inplace=True)
        vias_sec.drop_duplicates(subset='geometry', inplace=True)
        vias_sec['geometry'] = vias_sec.geometry.buffer(0)

        return vias_sec

    def crear_capas_parcelas(self, parcelas_municipio, vias_municipio):
        """
            Obtiene las capas de parcelas tanto totales como urbanas y rurales
            Guarda el shp de rurales y devuelve las totales

            :param parcelas_municipio: Capa de parcelas del municipio
            :type parcelas_municipio: Geodataframe

            :param vias_municipio: Capa vias del municipio
            :type vias_municipio: Geodataframe

            :return: Parcelas totales del municipio
            :rtype: Geodataframe
        """

        print("Transformar parcelas")
        parcelas_totales = parcelas_municipio

        # Si hay vias las parcelas totales serán la diferencia con las vias y el añadido de estas
        if not vias_municipio.empty:
            vias_municipio['geometry'] = vias_municipio.geometry.buffer(0.001)
            parcelas_totales = gpd.overlay(parcelas_municipio, vias_municipio.dissolve(), how='difference')

        parcelas_totales.reset_index(inplace=True, drop=True)
        parcelas_geom = parcelas_totales[parcelas_totales.geometry.type != 'Polygon']
        parcelas_geom = parcelas_geom.explode()

        parcelas_totales = parcelas_totales.append(parcelas_geom)
        parcelas_totales = parcelas_totales[parcelas_totales.geometry.type == 'Polygon']
        parcelas_totales['geometry'] = parcelas_totales.geometry.buffer(0)

        parcelas_totales.reset_index(inplace=True, drop=True)
        parcelas_totales.set_geometry(col='geometry', inplace=True)
        parcelas_totales.set_crs(parcelas_totales.crs, inplace=True)

        parcelas_totales['REFCAT'] = parcelas_totales.apply(lambda x: self.cambiar_refcat(), axis=1)

        # Devolvemos las parcelas
        return parcelas_totales

    def crear_capas_edificios(self, parcelas_municipio, capa_edificios):
        """
            Función que obtiene y guarda en la ruta correspondiente las capas de edificios de un municipio

            :param parcelas_municipio: Geodataframe de las parcelas que corresponden al municipio
            :type parcelas_municipio: Geodataframe

            :param capa_edificios: Geodataframe de los edificios que corresponden al municipio
            :type capa_edificios: Geodataframe

            :return: None
        """

        columnas = ['USO', 'TIPOPOL', 'PROP', 'CONSTRU', 'REFCAT', 'geometry']
        edificios = gpd.sjoin(capa_edificios, parcelas_municipio)

        columnas_totales = list(edificios.columns.values)

        edificios.drop(list(filter(lambda columna: columna not in columnas,  columnas_totales)), axis=1, inplace=True)
        edificios['REFCAT'] = edificios.apply(lambda x: self.cambiar_refcat(), axis=1)

        edificios['TIPOPOL'] = 'CONSTRUCCION'
        edificios['CONSTRU'] = 'EDIFICIO'

        edificios_urbanos = edificios[((edificios.USO == "URBANO") & (edificios.PROP == 'PRIVADO'))]
        edificios_rurales = edificios[((edificios.USO == "RURAL") & (edificios.PROP == 'PRIVADO'))]

        if not edificios_urbanos.empty:
            self.guardar_capas_sec(edificios_urbanos, 'constru_u_d')

        if not edificios_rurales.empty:
            self.guardar_capas_sec(edificios_rurales, 'constru_r_d')

    def cambiar_refcat(self):
        """
            Aumenta el valor de la referencia catastral y la devuelve

            :return: Referencia catastral actalizada
            :rtype: int

        """
        self.ref_cat_actual = self.ref_cat_actual + 1
        return "A%s" % self.ref_cat_actual

    def guardar_capas_sec(self, capa, nombre_capa, driver="GeoJSON"):
        """
            Función para crear shp a partir de un Geodataframe recibido.
            Escribirá también en el documento la capa creada

            :param capa: Geodataframe recibido que pasará a shp
            :type capa: Geodataframe

            :param nombre_capa: nombre de la capa
            :type nombre_capa: str

            :param driver: Formato en que se guardara el geodataframe
            :type driver: str

            :return: None
        """

        print("Guardando capa %s" % nombre_capa)
        try:
            # Creamos shp con elnombre recibido
            capa.to_file(self.directorio_ficheros_salida + '/%s.geojson' % nombre_capa, driver=driver)

        except Exception as error:

            print('Error', 'Error al escribir capa %s: %s' % (nombre_capa, error))
