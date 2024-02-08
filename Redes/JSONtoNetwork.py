import json
import geopandas as gpd
from shapely.geometry import Point, LineString
import os
import shutil
import tkinter as tk
from tkinter import filedialog

def seleccionar_carpeta(titulo="Seleccionar carpeta"):
    root = tk.Tk()
    root.withdraw()  # Ocultamos la ventana principal de Tkinter
    folder_selected = filedialog.askdirectory(title=titulo)  # Abrimos el diálogo para seleccionar la carpeta
    return folder_selected

def remove_unsupported_fields(attributes):
    for key, value in list(attributes.items()):
        if isinstance(value, (list, dict)):
            del attributes[key]
        else:
            attributes[key] = value
    return attributes

def process_json(json_path, output_dir, jsons_dir):
    try:
        # Copia el archivo JSON al directorio designado para almacenar los JSON utilizados
        shutil.copy(json_path, jsons_dir)

        with open(json_path, 'r') as file:
            data = json.load(file)

        # Crea una carpeta única para este conjunto de datos
        dataset_name = os.path.splitext(os.path.basename(json_path))[0]
        dataset_output_dir = os.path.join(output_dir, dataset_name)
        if not os.path.exists(dataset_output_dir):
            os.makedirs(dataset_output_dir)

        # Procesamiento de los datos
        cctt_points, nudos_points, tramos_lines = [], [], []
        for cct in data['cctt']:
            cct_copy = remove_unsupported_fields(cct.copy())
            cctt_points.append({'geometry': Point(cct['x'], cct['y']), **cct_copy})
            for nudo in cct['nudos']:
                nudo_copy = remove_unsupported_fields(nudo.copy())
                nudos_points.append({'geometry': Point(nudo['x'], nudo['y']), **nudo_copy})
            for tramo in cct['tramos']:
                tramo_copy = remove_unsupported_fields(tramo.copy())
                origen = next((n for n in cct['nudos'] if n['id'] == tramo['nudoorigen']), None)
                destino = next((n for n in cct['nudos'] if n['id'] == tramo['nudofin']), None)
                if origen and destino:
                    tramos_lines.append({'geometry': LineString([(origen['x'], origen['y']), (destino['x'], destino['y'])]), **tramo_copy})

        # Convertir datos a GeoDataFrames
        gdf_cctt = gpd.GeoDataFrame(cctt_points, geometry='geometry')
        gdf_nudos = gpd.GeoDataFrame(nudos_points, geometry='geometry')
        gdf_tramos = gpd.GeoDataFrame(tramos_lines, geometry='geometry')

        # Asegurar que los campos sean del tipo correcto en tramos
        for gdf, name in zip([gdf_cctt, gdf_nudos, gdf_tramos], ['cctt', 'nudos', 'tramos']):
            gdf.crs = "EPSG:32630"
            filename = os.path.join(dataset_output_dir, f"{name}.shp")
            gdf.to_file(filename)

    except Exception as e:
        print(f"Error al procesar {json_path}: {e}")

def find_json_in_subdirs():
    source_dir = seleccionar_carpeta("Seleccionar carpeta de origen")
    output_dir = seleccionar_carpeta("Seleccionar carpeta de destino")

    if not source_dir or not output_dir:
        print("Operación cancelada.")
        return

    # Crea una carpeta para almacenar todos los archivos JSON utilizados
    jsons_dir = os.path.join(output_dir, "JSON_usados")
    if not os.path.exists(jsons_dir):
        os.makedirs(jsons_dir)

    for root, dirs, files in os.walk(source_dir):
        if 'inputs' in dirs:
            entradas_path = os.path.join(root, 'inputs')
            json_files = [f for f in os.listdir(entradas_path) if f.endswith('d.json')]
            for json_file in json_files:
                json_path = os.path.join(entradas_path, json_file)
                try:
                    process_json(json_path, output_dir, jsons_dir)
                    print(f"Procesado y copiado: {json_file}")
                except Exception as e:
                    print(f"Error al procesar {json_file}: {e}")

if __name__ == "__main__":
    find_json_in_subdirs()
