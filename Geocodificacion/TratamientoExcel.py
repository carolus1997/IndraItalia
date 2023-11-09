import pandas as pd
import re
import json

def extract_data_from_excel(excel_path):
    # Leer el archivo Excel
    xls = pd.ExcelFile(excel_path)
    all_sheets_data = []

    # Iterar sobre cada hoja y extraer la información
    for sheet_name in xls.sheet_names:
        sheet_data = pd.read_excel(xls, sheet_name=sheet_name)
        # Aquí pondrías tu lógica de extracción específica...
        # Por ejemplo:
        address = sheet_data.loc[10, 'A'] # Suponiendo que la dirección está en fila 11, columna A
        phone = sheet_data.loc[10, 'AD'] # Suponiendo que el teléfono está en fila 11, columna AD
        active_capital = sheet_data.loc[36, 'Q'] # Suponiendo que el capital activo está en fila 37, columna Q

        # Extraer número del portal
        house_number_match = re.search(r'\b\d+\b', address)
        house_number = house_number_match.group(0) if house_number_match else "Unknown"

        # Añadir los datos extraídos a la lista
        all_sheets_data.append({
            'road': address.replace(house_number, '').strip(),
            'house_number': house_number,
            'phone': phone,
            'active_capital': active_capital,
            # Agregar más campos según sea necesario
        })

    return all_sheets_data

# Llamar a la función con la ruta del archivo Excel
excel_data = extract_data_from_excel('ruta/a/tu/archivo.xlsx')
# Suponiendo que `excel_data` es la lista de diccionarios que obtuviste del paso anterior

# Convertir los datos del Excel a JSON
json_data = json.dumps(excel_data, ensure_ascii=False, indent=4)

# Guardar el JSON en un archivo
with open('datos_excel.json', 'w', encoding='utf-8') as f:
    f.write(json_data)