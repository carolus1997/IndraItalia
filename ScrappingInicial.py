import requests
from bs4 import BeautifulSoup

# Ruta del certificado del servidor
cert_path = '/path/to/cert.pem'

# Realiza la solicitud HTTP GET a la página web
url = 'https://tinitaly.pi.ingv.it/Download_Area1_0.html'
response = requests.get(url, verify=cert_path)

# Analiza el contenido HTML de la página
soup = BeautifulSoup(response.content, 'html.parser')

# Encuentra todas las etiquetas 'area' dentro del mapa 'FPMap0'
areas = soup.select('map[name="FPMap0"] area')

# Crea una lista para almacenar los enlaces de descarga
enlaces_descarga = []

# Itera sobre las etiquetas 'area' y extrae los enlaces de descarga
for area in areas:
    enlace = area['href']
    if enlace.endswith('.zip'):
        enlaces_descarga.append(enlace)

# Descarga los archivos .zip
for enlace in enlaces_descarga:
    url_descarga = url + '/' + enlace
    nombre_archivo = enlace.split('/')[-1]

    # Realiza la solicitud HTTP GET al enlace de descarga
    response = requests.get(url_descarga)

    # Guarda el contenido de la respuesta en un archivo local
    with open(nombre_archivo, 'wb') as archivo:
        archivo.write(response.content)

    print(f"Archivo '{nombre_archivo}' descargado con éxito.")

print("Descarga completa.")
