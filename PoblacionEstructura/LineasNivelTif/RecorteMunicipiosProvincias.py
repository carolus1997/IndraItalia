import geopandas as gpd
import os

# Cargar el shapefile
ruta_shapefile = r'C:\Users\ctmiraperceval\Desktop\CartografiaPaises\Recursos\Recursos_Es\Limites_Admin\lineas_limite\SHP_ETRS89\recintos_municipales_inspire_peninbal_etrs89\recintos_municipales_inspire_peninbal_etrs89_modified.shp'
gdf = gpd.read_file(ruta_shapefile)

# Ruta base para guardar los archivos de salida
ruta_base = r'C:/Users/ctmiraperceval/Desktop/CartografiaPaises/Recursos/Recursos_Es/RecortesProvincias'

# Crear una capa por cada código de provincia
for codprov in gdf['CODPROV'].unique():
    # Filtrar por Provincia
    gdf_prov = gdf[gdf['CODPROV'] == codprov]

    # Ruta para guardar el shapefile de la provincia
    ruta_salida = os.path.join(ruta_base, f"{codprov}.shp")

    # Guardar la capa recortada
    gdf_prov.to_file(ruta_salida)

print("Capas de municipios recortadas por provincia creadas.")