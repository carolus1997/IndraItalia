import arcpy
import os

# Rutas de las capas de entrada
capa_roja = r"C:\Users\ctmiraperceval\OneDrive - Indra\Escritorio\CartoItalia\Data\Recursos\Edificios\hotosm_ita_central_buildings_polygons.shp"
capa_verde = r"C:\Users\ctmiraperceval\OneDrive - Indra\Escritorio\CartoItalia\Data\Recursos\Edificios\Edificios_Geofabrik"
capa_azul = r"C:\Users\ctmiraperceval\Documents\ArcGIS\Projects\CartoItalia\CartoItalia.gdb\EdificiosItaliaOSM"

# Asegurarse de que la ruta de salida exista
ruta_salida = r"C:\Users\ctmiraperceval\OneDrive - Indra\Escritorio\CartoItalia\Data\Recursos\Edificios"
if not os.path.exists(ruta_salida):
    os.makedirs(ruta_salida)

# Realizar la intersección entre la capa verde y la capa azul
capa_intermedia = arcpy.Intersect_analysis([capa_verde, capa_azul], os.path.join(ruta_salida, "capa_intermedia"))

# Agregar las entidades verdes a la capa intermedia si hay intersección
arcpy.Append_management(capa_verde, capa_intermedia, "NO_TEST")

# Realizar la intersección entre la capa roja y la capa intermedia
capa_final = arcpy.Intersect_analysis([capa_roja, capa_intermedia], os.path.join(ruta_salida, "capa_final"))

# Eliminar duplicados en la capa final
arcpy.DeleteIdentical_management(capa_final, ["SHAPE"])



