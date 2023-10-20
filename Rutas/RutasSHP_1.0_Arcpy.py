import arcpy
import os
# Establece el entorno
arcpy.env.workspace = r"D:\Minsait_Curro\Recursos_Por\Carreteras\PruebasRutas.gdb"  # Asegúrate de reemplazar con la ruta a tu geodatabase
arcpy.env.overwriteOutput = True

# Entradas
coord1 = input('Introduce las coordenadas del punto de inicio (Ej: 38.339366,-0.4907572): ').split(',')
coord2 = input('Introduce las coordenadas del punto de destino (Ej: 38.339366,-0.4907572): ').split(',')

# Asegúrate de que las coordenadas estén en formato float
x1, y1 = float(coord1[0]), float(coord1[1])
x2, y2 = float(coord2[0]), float(coord2[1])

# Crear puntos de inicio y destino
inicio = arcpy.PointGeometry(arcpy.Point(x1, y1))
destino = arcpy.PointGeometry(arcpy.Point(x2, y2))

# Crear una capa de puntos
arcpy.management.Merge([inicio, destino], os.path.join(r"D:\Minsait_Curro\Recursos_Por\Carreteras","PuntosRuta.shp"))

# Establecer el Dataset de Red
network_data_source = r"D:\Minsait_Curro\Recursos_Por\Carreteras\PruebasRutas.gdb\Red\PruebaRutaBasica"  # Reemplaza con la ruta a tu Dataset de Red

# Crear una capa de red
arcpy.na.MakeRouteLayer(network_data_source, "RutaLayer", "Length")

# Añadir los puntos a la capa de red
arcpy.na.AddLocations("RutaLayer", "Stops", "PuntosRuta.shp")

# Resolver la ruta
arcpy.na.Solve("RutaLayer")

# Exportar la ruta a una capa de salida
arcpy.management.CopyFeatures("RutaLayer\\Routes", "RutaSalida.shp")

print("Ruta calculada y guardada en 'RutaSalida.shp'")
