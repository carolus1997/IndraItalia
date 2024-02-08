import geopandas as gpd
import json
import os
import config

def shp_to_json_full(cctt_shp_path, nudos_shp_path, tramos_shp_path, output_json_path):
    try:
        gdf_cctt = gpd.read_file(cctt_shp_path)
        gdf_tramos = gpd.read_file(tramos_shp_path)

        print(f"Total CCTT: {len(gdf_cctt)}")
        print(f"Total Tramos: {len(gdf_tramos)}")

        # Preparación de los datos para el JSON
        cctt_data = [dict(row) for _, row in gdf_cctt.drop(columns='geometry').iterrows()]
        tramos_data = [dict(row) for _, row in gdf_tramos.drop(columns='geometry').iterrows()]

        # Asociar tramos a sus CCTTs correspondientes
        for cctt in cctt_data:
            cctt_tramos = [tramo for tramo in tramos_data if tramo['idcd'] == cctt['idcd']]
            cctt['tramos'] = cctt_tramos

        json_data = {"cctt": cctt_data}
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        return True, None  # Devuelve éxito y ningún error
    except Exception as e:
        return False, str(e)  # Devuelve fracaso y el mensaje de error

def process_subfolders(base_dir, output_dir):
    errores = []  # Lista para mantener los errores
    for root, dirs, files in os.walk(base_dir):
        for dir_name in dirs:
            if "_processed" in dir_name:
                cctt_shp_path = os.path.join(root, dir_name, "cctt.shp")
                nudos_shp_path = os.path.join(root, dir_name, "nudos.shp")
                tramos_shp_path = os.path.join(root, dir_name, "tramos_final.shp")
                if os.path.exists(cctt_shp_path) and os.path.exists(tramos_shp_path):
                    output_folder_name = dir_name.replace("_processed", "")
                    output_json_path = os.path.join(output_dir, f"{output_folder_name}.json")
                    exito, error = shp_to_json_full(cctt_shp_path, nudos_shp_path, tramos_shp_path, output_json_path)
                    if exito:
                        print(f"Archivo JSON creado para {output_folder_name}")
                    else:
                        errores.append((output_folder_name, error))  # Añadir el error a la lista

    # Manejar errores después de procesar todos los directorios
    if errores:
        print("Errores encontrados durante la ejecución:")
        for solicitud, error in errores:
            print(f"Solicitud: {solicitud}, Error: {error}")

if __name__ == "__main__":
    base_dir = config.BASE_DIR
    output_dir = config.JSON_SALIDAS_DIR
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    process_subfolders(base_dir, output_dir)
