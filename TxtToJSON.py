import json

# Carga el string desde el archivo de texto
with open('particelle.geojson.txt') as f:
    geojson_text = f.read()

# Convierte el string a un GeoJSON
geojson_data = json.loads(geojson_text)

# Guarda el GeoJSON en un archivo
with open('data.geojson', 'w') as f:
    json.dump(geojson_data, f)
