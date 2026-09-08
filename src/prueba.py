from funcion_importe_dataset import cargar_dataset_physionet
import matplotlib.pyplot as plt
import json
import os

df, info = cargar_dataset_physionet(db_name='mghdb', record_id='mgh001', sampfrom=0, sampto=1000)

#Definir la ruta para guardar el DataFrame y la información técnica
raw_dir = os.path.join('data', 'raw')
os.makedirs(raw_dir, exist_ok=True) #Crear el directorio si no existe

csv_path = os.path.join(raw_dir, 'mghdb_mgh001_raw.csv')
df.to_csv(csv_path, index=False)  # Guardar el DataFrame en un archivo CSV
print(f"Señales crudas guardadas en: {csv_path}")

info_clean = info.copy()
if 'raw_header_dict' in info_clean:
    del info_clean['raw_header_dict']
if info_clean.get('base_datetime'):
    info_clean['base_datetime'] = str(info_clean['base_datetime'])

json_path = os.path.join(raw_dir, "mghdb_mgh001_info_raw.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(info_clean, f, indent=4, ensure_ascii=False)
print(f"Información técnica guardada en: {json_path}")

# plt.plot(df['time [s]'], df[df.columns[1]])  # Graficar la primera señal
# plt.title(f'{df.columns[1]} vs Time')
# plt.xlabel('Time [s]')
# plt.ylabel('Signal')
# plt.show()