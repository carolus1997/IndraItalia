import geopandas as gpd

# Cambia esto a la ruta de tu shapefile original
shapefile_path = r"C:\Users\ctmiraperceval\Desktop\CartografiaPaises\Recursos\Recursos_Es\Limites_Admin\lineas_limite\SHP_ETRS89\recintos_municipales_inspire_peninbal_etrs89\recintos_municipales_inspire_peninbal_etrs89_modified.shp"
# Cargar el shapefile
gdf = gpd.read_file(shapefile_path)

# Verificar si el campo 'NATCODE' está presente
if 'NATCODE' in gdf.columns:
    # Crear un nuevo campo 'CODMUNI' con los últimos 5 caracteres de 'NATCODE'
    gdf['CODMUNI'] = gdf['NATCODE'].apply(lambda x: x[-5:])
    gdf['CODPROV'] = gdf['NATCODE'].apply(lambda x: x[4:6])
    gdf['CODCOM'] = gdf['NATCODE'].apply(lambda x: x[2:4])

    # Guardar en un nuevo shapefile
    output_path = r'C:\Users\ctmiraperceval\Desktop\CartografiaPaises\Recursos\Recursos_Es\Limites_Admin\lineas_limite\SHP_ETRS89\recintos_municipales_inspire_peninbal_etrs89\recintos_municipales_inspire_peninbal_etrs89_modified.shp'
    gdf.to_file(output_path)

    print("Shapefile modificado guardado en:", output_path)
else:
    print("El campo 'NATCODE' no se encuentra en la capa.")