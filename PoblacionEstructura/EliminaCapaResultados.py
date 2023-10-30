import arcpy
import os

arcpy.env.overwriteOutput = True

# Directorio donde se encuentran las geodatabases
gdb_directory = r"C:\Users\ctmiraperceval\OneDrive - Indra\Escritorio\CartoItalia\Data\Resultados\Gdbs_Es"

# Listar todas las geodatabases dentro del directorio
for root, dirs, files in os.walk(gdb_directory):
    for dir in dirs:
        if dir.endswith(".gdb"):  # Si es una geodatabase
            gdb_path = os.path.join(root, dir)

            # Establecer el espacio de trabajo en la geodatabase actual
            arcpy.env.workspace = gdb_path

            # Listar todos los datasets de la geodatabase
            datasets = arcpy.ListDatasets()
            for dataset in datasets:

                # Dentro de cada dataset, listar las capas de entidades
                fc_list = arcpy.ListFeatureClasses(feature_dataset=dataset)
                for fc in fc_list:
                    if "_Edificios" in fc:  # Si la capa tiene "_Edificios" en el nombre
                        fc_path = os.path.join(gdb_path, dataset, fc)

                        # Eliminar la capa
                        arcpy.Delete_management(fc_path)
                        print(f"Capa {fc_path} eliminada.")
