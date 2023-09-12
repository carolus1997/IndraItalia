import arcpy
import os
# Ruta de la carpeta que contiene los archivos .tif
tif_folder = r'C:\Users\ctmiraperceval\Desktop\CartoItalia\Data\Recursos\DEMs\Continente\Zips2'

# Ruta del archivo .shp de las regiones
shp_file = r'C:\Users\ctmiraperceval\Desktop\CartoItalia\Data\Recursos\Unidades_Admin_It\RegionesItaliaContinental.shp'

# Nombre del atributo que contiene los nombres de las regiones
attribute_name = 'NAME_1'

# Ruta de salida del archivo raster total
output_raster = r'C:\Users\ctmiraperceval\Desktop\CartoItalia\Data\Recursos\DEMs\Continente\Rasters\total.tif'

# Ruta de salida de los archivos raster recortados por región
output_folder = r'C:\Users\ctmiraperceval\Desktop\CartoItalia\Data\Recursos\DEMs\Continente\Rasters'
# Lista de archivos .tif en la carpeta
tif_files = [os.path.join(tif_folder, file) for file in os.listdir(tif_folder) if file.endswith('.tif')]

# Unir los archivos .tif en uno solo
arcpy.MosaicToNewRaster_management(input_rasters=";".join(tif_files),
                                   output_location=os.path.dirname(output_raster),
                                   raster_dataset_name_with_extension=os.path.basename(output_raster),
                                   coordinate_system_for_the_raster='',
                                   pixel_type='32_BIT_FLOAT',  # Ajustar el tipo de píxel según la escala de altura
                                   cellsize='',
                                   number_of_bands='1',
                                   mosaic_method='',
                                   mosaic_colormap_mode='')

# Obtener los nombres de las regiones del atributo especificado
region_names = [row[0] for row in arcpy.da.SearchCursor(shp_file, attribute_name)]

# Recortar el raster total por cada región
for region_name in region_names:
    # Nombre del raster recortado
    output_raster_name = f"Dem_{region_name}.tif"

    # Ruta de salida del raster recortado
    output_raster_path = os.path.join(output_folder, output_raster_name)

    # Recortar el raster total por la región actual
    arcpy.Clip_management(in_raster=output_raster,
                          out_raster=output_raster_path,
                          in_template_dataset=shp_file,
                          clipping_geometry='ClippingGeometry',
                          maintain_clipping_extent='NO_MAINTAIN_EXTENT')
