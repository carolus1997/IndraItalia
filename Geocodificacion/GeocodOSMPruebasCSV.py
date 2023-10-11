import csv
import requests
from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
import chardet

app = Flask(__name__)

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search?format=json&q="

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/geocode', methods=['POST'])
def geocode_address():
    address = request.form.get('address')
    url = NOMINATIM_URL + address
    response = requests.get(url)
    data = response.json()
    if data:
        coords = {
            'longitude': data[0]['lon'],
            'latitude': data[0]['lat']
        }
        return render_template('results.html', coords=coords)
    else:
        return "Dirección no encontrada"

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    # Leer el CSV y geocodificar las direcciones
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    # Decodificar el contenido del archivo usando 'ISO-8859-1'
    content = file.read().decode('ISO-8859-1')
    csv_reader = csv.reader(content.splitlines())
    next(csv_reader, None)  # skip the headers

    for row in csv_reader:
        address = f"{row[0]} {row[1]}, {row[2]},{row[5]}"
        print(f"Consultando dirección: {address}")
        url = NOMINATIM_URL + address
        response = requests.get(url)
        data = response.json()
        # Si data está vacío, imprimamos un mensaje
        if not data:
            print(f"No se encontraron datos para la dirección: {address}")
            continue
        if data:
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(data[0]['lon']), float(data[0]['lat'])]
                },
                "properties": {
                    "address": address
                }
            }
            geojson["features"].append(feature)

    # Guardar el GeoJSON en un archivo
    with open('Address.geojson', 'w') as f:
        json.dump(geojson, f)

    return send_from_directory(directory=os.getcwd(), path='Address.geojson', as_attachment=True, mimetype='application/json')

@app.route('/descargar_plantilla')
def descargar_plantilla():
    return send_from_directory(directory=os.getcwd(), filename='plantilla.txt', as_attachment=True, mimetype='text/csv')

@app.route('/upload_json', methods=['POST'])
def upload_json():
    # Verificar si el archivo fue enviado
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    # Leer y parsear el JSON
    data = json.load(file)

    # Convertir a GeoJSON
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    for entry in data:
        lat = float(entry['lat'])
        lon = float(entry['lon'])
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat]
            },
            "properties": entry['address']
        }
        geojson["features"].append(feature)

    # Guardar el GeoJSON en un archivo
    with open('output_from_json.geojson', 'w') as f:
        json.dump(geojson, f)

    return send_from_directory(directory=os.getcwd(), path='output_from_json.geojson', as_attachment=True, mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)
