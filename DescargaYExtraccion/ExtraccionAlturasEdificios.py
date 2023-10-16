import arcpy
import json
import os

# Define la función para extraer y convertir los datos
def extract_height(properties):
    data = json.loads(properties)
    height = data['height']
    height_str = str(height)
    return height_str.replace('.', ',')

# Define la ruta de la carpeta que deseas recorrer
workspace = r"C:\Users\ctmiraperceval\Desktop\CartoItalia\Data\Recursos\OSM_EXPORT"

# Recorre la carpeta y subcarpetas
for dirpath, dirnames, filenames in arcpy.da.Walk(workspace, datatype="FeatureClass"):
    for filename in filenames:
        # Define la ruta completa al shapefile
        fc = os.path.join(dirpath, filename)

        # Agrega un nuevo campo de tipo float llamado "altura" si no existe
        if 'altura' not in [f.name for f in arcpy.ListFields(fc)]:
            arcpy.AddField_management(fc, "altura", "FLOAT")

        # Usa un cursor de actualización para recorrer cada fila en el shapefile
        with arcpy.da.UpdateCursor(fc, ["properties", "altura"]) as cursor:
            for row in cursor:
                # Extrae y convierte los datos del campo "properties"
                altura = extract_height(row[0])

                # Actualiza el valor del campo "altura"
                row[1] = altura
                cursor.updateRow(row)
