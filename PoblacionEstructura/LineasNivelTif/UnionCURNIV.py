import arcpy
import os

# Establece la carpeta de trabajo
arcpy.env.workspace = r'C:\Users\ctmiraperceval\Desktop\CartografiaPaises\Recursos\Recursos_Es\BTN'

# Lista para almacenar las capas shapefile
capas_shapefile = []

# Busca capas shapefile con "CUR_NIV" en su nombre
for dirpath, dirnames, filenames in arcpy.da.Walk(arcpy.env.workspace, datatype="FeatureClass"):
    for filename in filenames:
        if filename.endswith(".shp") and "CUR_NIV" in filename:
            capas_shapefile.append(os.path.join(dirpath, filename))

# Define la ubicación y el nombre del archivo shapefile de salida
archivo_salida = r'C:\Users\ctmiraperceval\Desktop\CartografiaPaises\Recursos\Recursos_Es\Altimetria\CURV_NIV\capa_unida.shp'

# Utiliza la herramienta Merge de ArcPy para unir las capas
arcpy.Merge_management(inputs=capas_shapefile, output=archivo_salida)

print("Capas unidas con éxito en:", archivo_salida)
