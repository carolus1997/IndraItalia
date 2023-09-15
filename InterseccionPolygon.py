import arcpy
import os
# 1. Leer las capas
capa1 = r"C:\Users\ctmiraperceval\OneDrive - Indra\Escritorio\CartoItalia\Data\Recursos\Edificios\hotosm_ita_northeast_buildings_polygons.shp"
capa2 = r"C:\Users\ctmiraperceval\OneDrive - Indra\Escritorio\CartoItalia\Data\Recursos\Edificios\gis_osm_buildings_a_free_1.shp"
# Asegúrate de que la ruta de salida exista
ruta_salida = r"C:\Users\ctmiraperceval\OneDrive - Indra\Escritorio\CartoItalia\Data\Recursos\Edificios"
if not os.path.exists(ruta_salida):
    os.makedirs(ruta_salida)

# 2. Comparar geometrías y 3. Guardar entidades que intersecan
# Crear una capa temporal para las entidades que intersecan
capa_interseccion = arcpy.Intersect_analysis([capa1, capa2], os.path.join(ruta_salida, "capa_interseccion"))

# 4. Si no intersecan, guardar ambas entidades
# Crear una capa temporal para las entidades que no intersecan
capa_simetrica = arcpy.SymDiff_analysis(capa1, capa2, os.path.join(ruta_salida, "capa_simetrica"))

# Unir las dos capas temporales en una nueva capa
arcpy.Merge_management([capa_interseccion, capa_simetrica], os.path.join(ruta_salida, "capa_final"))
