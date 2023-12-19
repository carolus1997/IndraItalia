import arcpy
capa_carreteras = r"C:\Users\ctmiraperceval\Documents\ArcGIS\Projects\CartoSec\Chile.gdb\Carreteras"
carreteras_dict = {
    "unclassified": (0, "track"),
    "proposed": (0, "track"),
    "platform": (0, "track"),
    "path": (1, "track"),
    "road": (1, "track"),
    "service": (1, "track"),
    "track": (1, "residential"),
    "track_grade1": (1, "residential"),
    "track_grade2": (1, "residential"),
    "track_grade3": (1, "residential"),
    "track_grade4": (1, "residential"),
    "track_grade5": (1, "residential"),
    "cycleway": (2, "residential"),
    "footway": (2, "residential"),
    "step": (2, "residential"),
    "pedestrian": (2, "residential"),
    "living_street": (2, "residential"),
    "bridleway": (2, "residential"),
    "residential": (2, "residential"),
    "primary_link": (3, "primary"),
    "primary": (3, "primary"),
    "rest_area": (4, "secondary"),
    "secondary_link": (4, "secondary"),
    "secondary": (4, "secondary"),
    "tertiary_link": (5, "tertiary"),
    "tertiary": (5, "tertiary"),
    "trunk": (6, "motorway"),
    "trunk_link": (6, "motorway"),
    "services": (6, "motorway"),
    "motorway_link": (6, "motorway"),
    "motorway": (6, "motorway")
}
# Añade un campo numérico
arcpy.AddField_management(capa_carreteras, "Codigo", "SHORT")

# Definir una función que toma el nombre de una carretera y devuelve el código y el subtipo correspondientes
def get_codigo_subtipo(nombre_carretera):
    if nombre_carretera in carreteras_dict:
        return carreteras_dict[nombre_carretera]
    else:
        return (None, None)  # Devuelve (None, None) si el nombre de la carretera no está en el diccionario

# Ahora puedes usar esta función en la expresión que pasas a CalculateField_management()

# Código de la calculadora de campo para el campo "Codigo"
arcpy.CalculateField_management(capa_carreteras, "Codigo", "get_codigo_subtipo(!fclass!)[0]", "PYTHON3")

