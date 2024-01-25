import geopandas as gpd
import os

# Cargar el shapefile
ruta_shapefile = r'C:\Users\ctmiraperceval\Desktop\CartografiaPaises\Recursos\Recursos_Es\Limites_Admin\lineas_limite\SHP_ETRS89\recintos_municipales_inspire_peninbal_etrs89\recintos_municipales_inspire_peninbal_etrs89_modified.shp'
gdf = gpd.read_file(ruta_shapefile)

# Ruta base para la estructura de carpetas
ruta_base = r'C:/Users/ctmiraperceval/Desktop/CartografiaPaises/Recursos/Recursos_Es/Altimetria/TIF'

# Crear estructura de carpetas
for com in gdf['CODCOM'].unique():
    ruta_com = os.path.join(ruta_base, com)
    os.makedirs(ruta_com, exist_ok=True)

    # Filtrar por Comunidad
    gdf_prov = gdf[gdf['CODCOM'] == com]

    for prov in gdf_prov['CODPROV'].unique():
        ruta_prov = os.path.join(ruta_com, prov)
        os.makedirs(ruta_prov, exist_ok=True)

        # Filtrar por Provincia
        gdf_muni = gdf_prov[gdf_prov['CODPROV'] == prov]

        for muni in gdf_muni['CODMUNI'].unique():
            ruta_muni = os.path.join(ruta_prov, muni)
            os.makedirs(ruta_muni, exist_ok=True)

print("Estructura de carpetas creada.")
