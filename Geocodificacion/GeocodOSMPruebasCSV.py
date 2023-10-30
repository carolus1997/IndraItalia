import csv
import requests
import tempfile
from flask import Flask, render_template, request, send_from_directory
import os
import json
import time

app = Flask(__name__)

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search?format=json&q="

def format_address_from_row(row):
    """Construye una dirección formateada a partir de una fila de CSV."""
    return f"{row[2]} {row[1]}, {row[3]},{row[6]},{row[5]}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/geocode', methods=['POST'])
def geocode_address():
    address = request.form.get('address')
    coords = geocode_using_nominatim(address)
    if coords:
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

    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    content = file.read().decode('ISO-8859-1')
    csv_reader = csv.reader(content.splitlines())
    next(csv_reader, None)  # skip the headers

    for row in csv_reader:
        address = format_address_from_row(row)
        coords = geocode_using_nominatim(address)
        if coords:
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [coords['longitude'], coords['latitude']]
                },
                "properties": {
                    "address": address
                }
            }
            geojson["features"].append(feature)

    temp_file = tempfile.NamedTemporaryFile(delete=False)
    with open(temp_file.name, 'w') as f:
        json.dump(geojson, f)

    return send_from_directory(directory=os.path.dirname(temp_file.name), path=os.path.basename(temp_file.name), as_attachment=True, mimetype='application/json')

@app.route('/descargar_plantilla_csv')
def descargar_plantilla_csv():
    return send_from_directory(directory=os.path.join(os.getcwd(), 'templates'), path='plantilla.csv', as_attachment=True, mimetype='text/csv')

@app.route('/descargar_plantilla_json')
def descargar_plantilla_json():
    return send_from_directory(directory=os.path.join(os.getcwd(), 'templates'), path='plantilla.json', as_attachment=True, mimetype='application/json')

@app.route('/upload_json', methods=['POST'])
def upload_json():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    try:
        data = json.load(file)
    except:
        return "Error al leer el JSON. ¿Está en el formato correcto?"

    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    for entry in data:
        address = f"{entry['road']} {entry['house_number']}, {entry['city']}, {entry['county']}, {entry['postcode']}, {entry['country']}"
        coords = geocode_using_nominatim(address)
        if coords:
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [coords['longitude'], coords['latitude']]
                },
                "properties": {
                    "address": address
                }
            }
            geojson["features"].append(feature)
        time.sleep(1)  # espera 1 segundo antes de la siguiente solicitud

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".geojson")
    with open(temp_file.name, 'w') as f:
        json.dump(geojson, f)

    return send_from_directory(directory=os.path.dirname(temp_file.name), path=os.path.basename(temp_file.name), as_attachment=True, download_name="result.geojson", mimetype='application/geo+json')




def geocode_using_nominatim(address):
    try:
        response = requests.get(NOMINATIM_URL + address, timeout=10)
        data = response.json()
        if data:
            return {
                'longitude': float(data[0]['lon']),
                'latitude': float(data[0]['lat'])
            }
    except requests.RequestException as e:
        print(f"Error al geocodificar la dirección {address}: {e}")
    return None

if __name__ == '__main__':
    app.run(debug=True)
