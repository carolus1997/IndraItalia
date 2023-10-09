from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates"))
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search?format=json&q="

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/geocode', methods=['POST'])
def geocode_address():
    address = request.form.get('address')

    # URL para la API de Nominatim
    url = NOMINATIM_URL + address

    # Hacer la solicitud a la API
    response = requests.get(url)
    data = response.json()

    # Extraer las coordenadas del resultado (tomando el primer resultado como el más relevante)
    if data:
        coords = {
            'latitude': data[0]['lat'],
            'longitude': data[0]['lon']
        }
        return render_template('results.html', coords=coords)
    else:
        return "Dirección no encontrada"

if __name__ == '__main__':
    app.run(debug=True)
