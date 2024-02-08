import arcpy
import os

arcpy.env.overwriteOutput = True

def crear_carpeta(carpeta):
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

carpeta_poligonos = r"C:\Users\ctmiraperceval\Desktop\CartografiaPaises\Recursos\Recursos_Es\RecortesProvincias\Poligonos"
carpeta_curvas_nivel = r"C:\Users\ctmiraperceval\Desktop\CartografiaPaises\Recursos\Recursos_Es\Altimetria\CUR_NIV_2"
carpeta_salida = r"C:\Users\ctmiraperceval\Desktop\CartografiaPaises\Recursos\Recursos_Es\Altimetria\CUR_NIV_MUNI"

arcpy.env.workspace = carpeta_poligonos
featureclassesPoligonos = arcpy.ListFeatureClasses()
arcpy.env.workspace = carpeta_curvas_nivel
featureclassesCurvasNivel = arcpy.ListFeatureClasses()

# Crear diccionario de concordancias
concordancias = {} 
for poligono in featureclassesPoligonos:
    identificador_poligono = poligono.split('.')[0]
    for curva in featureclassesCurvasNivel:
        identificador_curva = curva.split('_')[0]
        if identificador_poligono == identificador_curva:
            concordancias.setdefault(poligono, []).append(curva)

# Procesar cada concordancia
for poligono, curvas in concordancias.items():
    ruta_poligono = os.path.join(carpeta_poligonos, poligono)
    for curva in curvas:
        ruta_curva = os.path.join(carpeta_curvas_nivel, curva)

        with arcpy.da.SearchCursor(ruta_poligono, ["CODPROV", "CODMUNI"]) as cursor:
            for fila in cursor:
                codprov, codmuni = fila
                carpeta_prov = os.path.join(carpeta_salida, codprov)
                crear_carpeta(carpeta_prov)

                # Seleccionar y recortar por cada término municipal
                where_clause = f"CODMUNI = '{codmuni}'"
                arcpy.MakeFeatureLayer_management(ruta_poligono, "poligono_lyr", where_clause)
                arcpy.MakeFeatureLayer_management(ruta_curva, "curva_lyr")

                ruta_salida = os.path.join(carpeta_prov, f"{codmuni}.shp")
                arcpy.analysis.Intersect(["poligono_lyr", "curva_lyr"], ruta_salida)

                # Verificar si la capa de salida tiene entidades
                count = int(arcpy.management.GetCount(ruta_salida)[0])
                if count > 0:
                    print(f"Recorte guardado: {ruta_salida}, con {count} entidades.")
                else:
                    print(f"No se encontraron intersecciones para {codmuni} en {curva}")

                arcpy.Delete_management("poligono_lyr")
                arcpy.Delete_management("curva_lyr")

print("Proceso completado.")
