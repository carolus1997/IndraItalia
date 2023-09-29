import arcpy
import os
arcpy.env.overwriteOutput = True
# Rutas de las capas de entrada
capa_roja = r"C:\Users\ctmiraperceval\OneDrive - Indra\Escritorio\CartoItalia\Data\Recursos\Edificios\Edificios.gdb\hotosm_ita_central_buildings_polygons"
capa_verde = r"C:\Users\ctmiraperceval\Documents\ArcGIS\Projects\CartoItalia\CartoItalia.gdb\Edificios_Geofabrik_Italia"
capa_azul = r"C:\Users\ctmiraperceval\OneDrive - Indra\Escritorio\CartoItalia\Data\Recursos\Edificios\Edificios.gdb\EdificiosItaliaOSM"

# Asegurarse de que la ruta de salida exista
ruta_salida = r"C:\Users\ctmiraperceval\OneDrive - Indra\Escritorio\CartoItalia\Data\Recursos\Edificios\Edificios.gdb"
if not os.path.exists(ruta_salida):
    os.makedirs(ruta_salida)

# Crear una capa intermedia para la intersección entre capa_roja y capa_verde
capa_intermedia_verde = arcpy.Intersect_analysis([capa_roja, capa_verde], os.path.join(ruta_salida, "capa_intermedia_verde"))

# Crear una capa intermedia para la intersección entre capa_roja y capa_azul
capa_intermedia_azul = arcpy.Intersect_analysis([capa_roja, capa_azul], os.path.join(ruta_salida, "capa_intermedia_azul"))

# Actualizar los valores de 'altura' en capa_roja con los valores correspondientes de capa_intermedia_verde y capa_intermedia_azul
with arcpy.da.UpdateCursor(capa_roja, ['altura']) as cursor_roja:
    for row_roja in cursor_roja:
        with arcpy.da.SearchCursor(capa_intermedia_verde, ['altura']) as cursor_intermedia_verde:
            for row_intermedia_verde in cursor_intermedia_verde:
                if row_roja[0] == row_intermedia_verde[0]:
                    row_roja[1] = row_intermedia_verde[1]
                    cursor_roja.updateRow(row_roja)
        with arcpy.da.SearchCursor(capa_intermedia_azul, ['altura']) as cursor_intermedia_azul:
            for row_intermedia_azul in cursor_intermedia_azul:
                if row_roja[0] == row_intermedia_azul[0]:
                    row_roja[1] = row_intermedia_azul[1]
                    cursor_roja.updateRow(row_roja)

# Agregar los edificios de capa_verde y capa_azul que no intersectan con capa_roja a capa_roja
capa_simetrica_verde = arcpy.SymDiff_analysis(capa_verde, capa_roja, os.path.join(ruta_salida, "capa_simetrica_verde"))
capa_simetrica_azul = arcpy.SymDiff_analysis(capa_azul, capa_roja, os.path.join(ruta_salida, "capa_simetrica_azul"))
arcpy.Append_management(capa_simetrica_verde, capa_roja, "NO_TEST")
arcpy.Append_management(capa_simetrica_azul, capa_roja, "NO_TEST")

# Agregar los campos faltantes de capa_verde y capa_azul a capa_roja
campos_capa_verde = arcpy.ListFields(capa_verde)
campos_capa_azul = arcpy.ListFields(capa_azul)
campos_capa_roja = arcpy.ListFields(capa_roja)

for campo in campos_capa_verde + campos_capa_azul:
    if campo not in campos_capa_roja:
        arcpy.AddField_management(capa_roja, campo.name, campo.type)