import arcpy
import os
import unidecode

def normalizar_nombre(nombre):
    return unidecode.unidecode(nombre.lower().replace(" ", ""))

def crear_carpeta(carpeta):
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

carpeta_poligonos = r"C:\Users\ctmiraperceval\Desktop\CartografiaPaises\Recursos\Recursos_Es\RecortesProvincias"
carpeta_curvas_nivel = r"C:\Users\ctmiraperceval\Desktop\CartografiaPaises\Recursos\Recursos_Es\Altimetria\CURV_NIV"
carpeta_salida = r"C:\Users\ctmiraperceval\Desktop\CartografiaPaises\Recursos\Recursos_Es\Altimetria\CUR_NIV_MUNI"

# Verificar si las carpetas existen
for carpeta in [carpeta_poligonos, carpeta_curvas_nivel, carpeta_salida]:
    if not os.path.exists(carpeta):
        print(f"La carpeta {carpeta} no existe. Verifique la ruta.")
        exit(1)  # Detiene la ejecución del script

# Configurar el entorno de trabajo de arcpy
arcpy.env.workspace = carpeta_curvas_nivel
arcpy.env.overwriteOutput = True  # Sobrescribir los archivos existentes

# Listar los archivos shapefile
curvas_nivel_archivos = [f for f in os.listdir(carpeta_curvas_nivel) if f.endswith('.shp')]

# Cargar polígonos municipales
poligonos = arcpy.ListFeatureClasses("*", "Polygon", carpeta_poligonos)

for poligono in poligonos:
    try:
        poligono_propiedades = arcpy.Describe(poligono)
        nombre_provincia = normalizar_nombre(poligono_propiedades.NAMEPROV)
        codprov = poligono_propiedades.CODPROV
        codmuni = poligono_propiedades.CODMUNI

        ruta_carpeta_codprov = os.path.join(carpeta_salida, codprov)
        crear_carpeta(ruta_carpeta_codprov)

        for archivo in curvas_nivel_archivos:
            if nombre_provincia in normalizar_nombre(archivo):
                curva_nivel = os.path.join(carpeta_curvas_nivel, archivo)

                # Asegurarse de que ambos tengan el mismo CRS
                arcpy.DefineProjection_management(curva_nivel, poligono_propiedades.spatialReference)

                # Realizar el recorte
                curva_recortada = arcpy.analysis.Intersect([curva_nivel, poligono], "in_memory/intersect")

                # Guardar el resultado
                ruta_archivo_salida = os.path.join(ruta_carpeta_codprov, f"{codmuni}.shp")
                arcpy.CopyFeatures_management(curva_recortada, ruta_archivo_salida)

    except arcpy.ExecuteError:
        print(arcpy.GetMessages(2))

    except Exception as e:
        print(f"Error: {e}")

print("Proceso completado.")

