import arcpy

def custom_clip(input_layer, overlay_layer, output_gdb, name_field="NAME_2"):
    """
    Función que simula la operación de recorte usando un select by location.
    La capa superpuesta se utiliza para seleccionar entidades en la capa de entrada y se guarda cada selección en una GDB.

    Parameters:
    - input_layer: Ruta de la capa de entrada que queremos recortar.
    - overlay_layer: Ruta de la capa que se superpondrá y que contiene las provincias.
    - output_gdb: Ruta de la geodatabase de salida donde se guardarán las capas recortadas.
    - name_field: Campo de la capa superpuesta que contiene los nombres de las provincias. Por defecto es "NAME_2".
    """

    # Establecer la geodatabase de salida como espacio de trabajo predeterminado
    arcpy.env.workspace = output_gdb

    # Hacer una lista de todos los valores únicos en el campo NAME_2 de la capa superpuesta
    with arcpy.da.SearchCursor(overlay_layer, name_field) as cursor:
        names = sorted({row[0] for row in cursor})

    # Para cada nombre en la lista de provincias
    for name in names:
        # Seleccione la provincia actual usando una consulta
        where_clause = f"{name_field} = '{name}'"
        arcpy.SelectLayerByAttribute_management(overlay_layer, "NEW_SELECTION", where_clause)

        # Seleccione las entidades en la capa de entrada que están completamente dentro de la provincia seleccionada
        arcpy.SelectLayerByLocation_management(in_layer=input_layer,
                                               overlap_type="WITHIN",
                                               select_features=overlay_layer)

        # Exportar las entidades seleccionadas a la GDB
        cleaned_name = name.replace(" ", "_").replace("-", "_").replace("/", "")
        output_name = f"{arcpy.Describe(input_layer).baseName}_{cleaned_name}"
        print(f"Intentando crear la capa: {output_name} en {output_gdb}")
        arcpy.CopyFeatures_management(input_layer, output_name)

        # Limpiar la selección para la siguiente iteración
        arcpy.SelectLayerByAttribute_management(overlay_layer, "CLEAR_SELECTION")
        arcpy.SelectLayerByLocation_management(input_layer, "CLEAR_SELECTION")

if __name__ == "__main__":
    input_layer_path = r"C:\Users\ctmiraperceval\OneDrive - Indra\Escritorio\CartoItalia\Data\Recursos_Es\Hidrografia\CuerposAgua_España.shp"
    overlay_layer_path = r"C:\Users\ctmiraperceval\OneDrive - Indra\Escritorio\CartoItalia\Data\Recursos_Es\Limites_Admin\Limites_Admin.gdb\recintos_provinciales_inspire_peninbal_etrs89"
    output_gdb_path = r"C:\Users\ctmiraperceval\OneDrive - Indra\Escritorio\CartoItalia\Data\Recursos_Es\Hidrografia\CuerposAgua.gdb"

    custom_clip(input_layer_path, overlay_layer_path, output_gdb_path)
