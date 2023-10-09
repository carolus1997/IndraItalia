from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search?format=json&q="

@app.route('/geocode/address', methods=['POST'])
def geocode_address():
    address = request.json.get('address')

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
        return jsonify(coords)
    else:
        return jsonify({"error": "Dirección no encontrada"}), 404

if __name__ == '__main__':
    app.run(debug=True)
