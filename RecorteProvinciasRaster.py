import arcpy
import os

arcpy.env.overwriteOutput = True

# Define las rutas de las capas de entrada, la capa de provincias y el geodatabase de salida
capa_type = input("Introduce el tipo de capa que vas a usar (ej. rios, carreteras, etc): ")
capa_entrada = input("Introduce la ruta de la capa a recortar: ")
capa_provincias = input("Introduce la ruta de la capa de provincias: ")
gdb_output = input("Introduce la ruta de la gdb de destino: ")
gdb_name = input("Introduce el nombre de la gdb de destino: ")
gdb_salida = os.path.join(gdb_output,gdb_name)
if arcpy.Exists(gdb_salida):
    print("Tu gdb ya existe")
    vaciado = input(
        "¿Quieres hacerle un vaciado de seguridad,(Responde usando mayusculas)? ")
    if vaciado == 'SI':
        arcpy.env.workspace = gdb_salida
        featureclasses_existentes = arcpy.ListFeatureClasses()
        for featureClass in featureclasses_existentes:
            arcpy.management.DeleteFeatures(featureClass)
        print(f"Se han eliminado todos los elementos de {gdb_name}")
    elif vaciado == 'NO':
        print("Perfecto, dejamos tu gdb intacta")
else:
    print("Tu gdb no existe")
    input_pregunta_gdb = input(f"¿Quieres usar la ruta {gdb_output} ?")
    if input_pregunta_gdb == 'SI':
        input_name_gdb = input(
            "Introduce el nombre de la GDB que vas a crear: ")
        arcpy.management.CreateFileGDB(gdb_output, input_name_gdb)
        print(f"Se ha creado una .gdb con el nombre: {input_name_gdb}")
    elif input_pregunta_gdb == 'NO':
        input_new_gdb = input("Introduce la ruta de la GDB que vas a crear: ")
        new_gdb = input_new_gdb
        print(new_gdb)
        input_name_gdb = input(
            "Introduce el nombre de la GDB que vas a crear: ")
        new_name = f"{input_name_gdb}.gdb"
        print(new_name)
        arcpy.management.CreateFileGDB(new_gdb, new_name)
        print(f"Se ha creado una .gdb con el nombre: {input_name_gdb}")

# Crea una capa temporal de la capa de provincias
arcpy.MakeFeatureLayer_management(capa_provincias, 'provincias_lyr')

# Obtiene una lista de las provincias en la capa de provincias
provincias = [row[0] for row in arcpy.da.SearchCursor('provincias_lyr', 'NAME_1')]

# Sustituye las comillas simples en los nombres de las provincias por un carácter de escape de comilla simple
provincias_escaped = [provincia.replace("'", "_") for provincia in provincias]

# Recorre cada provincia
for provincia in provincias_escaped:
    # Selecciona la provincia actual
    arcpy.SelectLayerByAttribute_management('provincias_lyr', 'NEW_SELECTION', f"NAME_1 = '{provincia}'")

    # Define el nombre del raster de salida
    nombre_raster_salida = f"{capa_type}_{provincia}"
    nombre_raster_salida = nombre_raster_salida.replace(" ", "_").replace("-", "_")
    raster_salida = os.path.join(gdb_salida, nombre_raster_salida)

    # Recorta el raster de entrada según los límites de la provincia actual y guarda el resultado en el raster de salida
    arcpy.Clip_management(capa_entrada, "#", raster_salida, 'provincias_lyr', "#", "ClippingGeometry", "NO_MAINTAIN_EXTENT")

# Elimina la capa temporal de provincias
arcpy.Delete_management('provincias_lyr')

print("PROCESO TERMINADO")
