import arcpy
import os
import zipfile
import shutil
arcpy.env.overwriteOutput = True
# Paso 1: Leer todos los archivos en una carpeta dada
carpeta = input("Introduzca la ruta de la carpeta: ")
archivos = os.listdir(carpeta)

# Paso 2: Descomprimir las carpetas comprimidas
for archivo in archivos:
    if archivo.endswith('.zip'):
        with zipfile.ZipFile(carpeta + '/' + archivo, 'r') as zip_ref:
            zip_ref.extractall(carpeta)


# Paso 3: Lista de rasters de cada carpeta y unirlos en una sola

carpetaRasters = input("Introduzca la ruta de la carpeta donde se van a guardar los rasters: ")

# Recorre todas las subcarpetas y archivos
for directorio_actual, subdirectorios, archivos in os.walk(carpeta):
    # Filtra las subcarpetas que no terminan con .zip
    subdirectorios[:] = [subdir for subdir in subdirectorios if not subdir.endswith('.zip')]

    for archivo in archivos:
        if not archivo.endswith('.zip'):
            # Obtiene la ruta completa del archivo actual
            ruta_archivo_actual = os.path.join(directorio_actual, archivo)

            # Crea la ruta de destino en la carpeta final
            ruta_destino = os.path.join(carpetaRasters, archivo)

            # Copia el archivo a la carpeta final
            shutil.copy2(ruta_archivo_actual, ruta_destino)

print("Archivos copiados exitosamente a la carpeta final.")
arcpy.env.workspace = carpetaRasters
rasters = arcpy.ListRasters("*", "TIF")

# Iterar sobre cada raster y calcular las estadísticas
for raster in rasters:
    arcpy.CalculateStatistics_management(raster)
    arcpy.management.BuildPyramids(raster)


# # Crear la geodatabase para los rasters
# input_new_gdb = input("Introduce la ruta de la GDB  que vas a crear: ")
# new_gdb = input_new_gdb
# input_name_gdb = input(
#     "Introduce el nombre de la GDB que vas a crear: ")
# new_name = "{}.gdb".format(input_name_gdb)
# arcpy.management.CreateFileGDB(new_gdb, new_name)
# print("Se ha creado una .gdb con el nombre: {}".format(input_name_gdb))
#
# # Crear un Mosaic Dataset
# input_name_Mosaic = input(
#     "Introduce el nombre del mosaico que vas a crear: ")
# with arcpy.EnvManager(outputCoordinateSystem='PROJCS["WGS_1984_Web_Mercator_Auxiliary_Sphere",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Mercator_Auxiliary_Sphere"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",0.0],PARAMETER["Standard_Parallel_1",0.0],PARAMETER["Auxiliary_Sphere_Type",0.0],UNIT["Meter",1.0]]'):
#     arcpy.management.CreateMosaicDataset(
#         in_workspace=os.path.join(new_gdb, new_name),
#         in_mosaicdataset_name=input_name_Mosaic,
#         coordinate_system='PROJCS["WGS_1984_Web_Mercator_Auxiliary_Sphere",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Mercator_Auxiliary_Sphere"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",0.0],PARAMETER["Standard_Parallel_1",0.0],PARAMETER["Auxiliary_Sphere_Type",0.0],UNIT["Meter",1.0]]',
#         num_bands=None,
#         pixel_type="",
#         product_definition="NONE",
#         product_band_definitions=None
#     )
# #arcpy.CreateMosaicDataset_management(os.path.join(new_gdb, new_name), input_name_Mosaic, r"C:\Users\ctmiraperceval"
# #                                                                                        r"\Desktop\CartoItalia\Data"
# #                                                                                        r"\Recursos\DEMs\Islas\4326"
# #                                                                                        r".prj", "1")
#
# # Ruta de la geodatabase con el Mosaic Dataset
# geodatabase = os.path.join(new_gdb, new_name)
#
# # Agregar los rasters al Mosaic Dataset
# for raster in rasters:
#     arcpy.AddRastersToMosaicDataset_management(geodatabase + "/" + input_name_Mosaic, "Raster Dataset", raster, "UPDATE_CELL_SIZES", "UPDATE_BOUNDARY", "UPDATE_OVERVIEWS", -1, 100, 1500, "", "", "", "ALLOW_DUPLICATES", "BUILD_PYRAMIDS", "CALCULATE_STATISTICS", "NO_THUMBNAILS", "", "NO_FORCE_SPATIAL_REFERENCE")
# print('Rasters añadidos al mosaico')
#
#
#
# # Ruta del Mosaic Dataset
# mosaic_dataset = "C:/ruta/de/la/geodatabase.gdb/MosaicDatasetName"
#
# # Ruta de la capa de provincias
# capa_provincias = "C:/ruta/de/la/capa_de_provincias.shp"
#
# # Ruta de la carpeta donde se guardarán los rasters recortados
# carpeta_recortes = "C:/ruta/de/la/carpeta_recortes"
#
# # Obtener una lista de provincias
# provincias = arcpy.da.SearchCursor(capa_provincias, ["Nombredelaprovincia"])
#
# # Iterar sobre cada provincia
# for provincia in provincias:
#     nombre_provincia = provincia[0]
#     # Crear una carpeta para la provincia
#     ruta_provincia = os.path.join(carpeta_recortes, nombre_provincia)
#     os.mkdir(ruta_provincia)
#
#     # Crear una geodatabase para la provincia
#     geodatabase_provincia = os.path.join(ruta_provincia, nombre_provincia + ".gdb")
#     arcpy.CreateFileGDB_management(ruta_provincia, nombre_provincia)
#
#     # Recortar el raster de la provincia
#     raster_recortado = os.path.join(geodatabase_provincia, "DEM_" + nombre_provincia)
#     arcpy.Clip_management(mosaic_dataset, "#", raster_recortado, capa_provincias, "#", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
#
