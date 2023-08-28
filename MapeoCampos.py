import arcpy
import pandas as pd

try:
    # Obtener el mapa actual
    aprx = arcpy.mp.ArcGISProject("CURRENT")
    map = aprx.activeMap

    # Crear una lista vacía para almacenar la información del campo
    field_info_list = []

    # Recorrer cada capa en el mapa
    for layer in map.listLayers():

        # Recorrer cada campo en la capa
        for field in arcpy.ListFields(layer):

            # Obtener la información del campo
            field_info = {
                "Capa": layer.name,
                "Nombre de campo": field.name,
                "Alias": field.aliasName,
                "Tipo de campo": field.type,
                "Longitud de campo": field.length
            }

            # Agregar la información del campo a la lista
            field_info_list.append(field_info)

    # Convertir la lista en un DataFrame de pandas
    df = pd.DataFrame(field_info_list)

    # Especificar el nombre del archivo Excel
    excel_file = "carreteras_info.xlsx"

    # Exportar el DataFrame a Excel
    df.to_excel(excel_file, index=False)

except PermissionError:
    print("No se puede escribir en el archivo. Asegúrese de que el archivo no esté abierto en otra aplicación y que tenga los permisos adecuados para escribir en el archivo.")
