#Importar librerías necesarias
import wfdb
import numpy as np
import pandas as pd
from typing import Tuple, Dict, Any, Optional
import matplotlib.pyplot as plt

def cargar_dataset_physionet(db_name: str, 
                             record_id: str, 
                             sampfrom: int = 0, 
                             sampto: Optional[int] = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Carga un registro de un dataset de PhysioNet y devuelve las señales físicas en un DataFrame de pandas
    junto con la información técnica asociada.

    Args:
        db_name (str): Nombre del dataset en PhysioNet.
        record_id (str): Identificador del registro a cargar.
        sampfrom (int, optional): Índice de la muestra desde la cual cargar las señales. Por defecto es 0.
        sampto (int, optional): Índice de la muestra hasta la cual cargar las señales. Si es None, 
                                se cargan todas las muestras.
    
    Returns:
        Tuple[pd.DataFrame, Dict[str, Any]]: Un DataFrame con las señales físicas y un diccionario con 
                                             la información técnica asociada.
    """
    print(f"Descargando dataset '{record_id}' desde '{db_name}'...")

    # Nombre del Dataset a trabajar (PhysioNet)
    record = wfdb.rdrecord(record_name=record_id,
                           pn_dir=db_name, 
                           sampfrom=sampfrom, 
                           sampto=sampto)
    
    #Extraer matriz de señales y frecuencia de muestreo
    signals = record.p_signal
    fs = record.fs

    #Construir vector de tiempo en segundos
    time_vector = np.arange(signals.shape[0]) / fs #shape[0] es el número de muestras

    #Asignar nombre a las columnas
    columns_name = []
    for sig_name, unit in zip(record.sig_name, record.units):
        unidad_str = unit if unit else 'desconocida'
        columns_name.append(f'{sig_name} ({unidad_str})')

    #Crear DataFrame con las señales y el vector de tiempo
    df = pd.DataFrame(signals, columns=columns_name)
    df.insert(0, 'time [s]', time_vector)

    # Compilar la información técnica y metadatos en un diccionario
    info_dict = {
        'record_name': record.record_name,
        'db_name': db_name,
        'sampling_frequency_hz': fs,
        'num_channels': record.n_sig,
        'total_samples_loaded': record.sig_len,
        'duration_seconds': record.sig_len / fs,
        'signals_info': [
            {'index': i, 'name': name, 'unit': unit} 
            for i, (name, unit) in enumerate(zip(record.sig_name, record.units))
        ],
        'comments': record.comments,
        'base_datetime': record.base_datetime,
        'raw_header_dict': record.__dict__
    }

    return df, info_dict