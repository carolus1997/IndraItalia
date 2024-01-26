import geopandas as gpd
import os

# Lista de códigos de provincia y nombres de provincia
lista_provincias = [['ArabaAlava', '01'], ['Albacete', '02'], ['AlacantAlicante', '03'], ['Almeria', '04'], ['Avila', '05'],
                    ['Badajoz', '06'], ['IllesBalears', '07'], ['Barcelona', '08'], ['Burgos', '09'], ['Caceres', '10'], ['Cadiz', '11'],
                    ['CastelloCastellon', '12'], ['CiudadReal', '13'], ['Cordoba', '14'], ['ACoruña', '15'], ['Cuenca', '16'], ['Girona', '17'],
                    ['Granada', '18'], ['Guadalajara', '19'], ['Gipuzkoa', '20'], ['Huelva', '21'], ['Huesca', '22'], ['Jaen', '23'],
                    ['Leon', '24'], ['Lleida', '25'], ['LaRioja', '26'], ['Lugo', '27'], ['Madrid', '28'], ['Malaga', '29'], ['Murcia', '30'],
                    ['Navarra', '31'], ['Ourense', '32'], ['Asturias', '33'], ['Palencia', '34'], ['Pontevedra', '36'], ['Salamanca', '37'],
                    ['Cantabria', '39'], ['Segovia', '40'], ['Sevilla', '41'], ['Soria', '42'], ['Tarragona', '43'], ['Teruel', '44'],
                    ['Toledo', '45'], ['ValenciaValencia', '46'], ['Valladolid', '47'], ['Bizkaia', '48'], ['Zamora', '49'], ['Zaragoza', '50'],
                    ['Ceuta', '51'], ['Melilla', '52'], ['Territorio no asociado a ninguna provincia', '54']]

# Crear un diccionario para mapear códigos de provincia a nombres de provincia
codigo_a_nombre = {prov[1]: prov[0] for prov in lista_provincias}

# Ruta de la carpeta que contiene las capas de polígonos municipales
carpeta_poligonos = r"C:\Users\ctmiraperceval\Desktop\CartografiaPaises\Recursos\Recursos_Es\RecortesProvincias\Poligonos"

# Comprobar si la carpeta existe
if os.path.isdir(carpeta_poligonos):
    for nombre_archivo in os.listdir(carpeta_poligonos):
        if nombre_archivo.endswith(".shp"):
            try:
                ruta_archivo = os.path.join(carpeta_poligonos, nombre_archivo)
                poligonos = gpd.read_file(ruta_archivo)

                # Asumiendo que 'CODPROV' es un campo en la capa y cada municipio tiene su código
                poligonos['NAMEPROV'] = poligonos['CODPROV'].map(codigo_a_nombre)

                # Verificar si hay municipios sin nombre de provincia asignado
                if poligonos['NAMEPROV'].isnull().any():
                    print(f"Advertencia: Algunos municipios en el archivo {nombre_archivo} no tienen un nombre de provincia asignado.")

                # Sobrescribir la capa existente con los cambios
                poligonos.to_file(ruta_archivo)
                print(f"Procesado: {nombre_archivo}")

            except Exception as e:
                print(f"Error al procesar el archivo {nombre_archivo}: {e}")
else:
    print(f"La carpeta '{carpeta_poligonos}' no existe.")

print("Se ha agregado el campo 'NAMEPROV' en todas las capas de polígonos municipales correspondientes.")