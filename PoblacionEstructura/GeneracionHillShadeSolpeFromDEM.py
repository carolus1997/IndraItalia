import arcpy
import os

# Define la carpeta fuente
carpeta_fuente = r"C:\Users\ctmiraperceval\Desktop\CartografiaPaises\Resultados\Gdbs_Chi"  # Reemplaza con la ruta de tu carpeta

# Lista todas las geodatabases en la carpeta fuente
gdb_list = [os.path.join(carpeta_fuente, f) for f in os.listdir(carpeta_fuente) if f.endswith(".gdb")]

# Procesa cada geodatabase
for gdb in gdb_list:
    try:
        arcpy.env.workspace = gdb
        rasters = arcpy.ListRasters()

        if rasters:
            for raster in rasters:
                # Asumiendo que el raster es un DEM
                base_name = os.path.splitext(raster)[0]
                hillshade_name = base_name.replace("DEM", "Hillshade")
                slope_name = base_name.replace("DEM", "Slope")

                # Crear hillshade
                arcpy.ddd.HillShade(raster, hillshade_name)

                # Crear slope
                arcpy.ddd.Slope(raster, slope_name)
        else:
            print(f"No se encontraron rasters en {gdb}")

    except Exception as e:
        print(f"Error procesando {gdb}: {e}")

print("Proceso completado.")
