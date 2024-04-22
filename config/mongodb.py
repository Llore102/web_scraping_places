import pandas as pd
from datetime import datetime
import math
from config.config import conn, mongo_uri

#! INSEETAR DATOS EN LA BD


async def insert_data_products(csv_file_path: str):
    try:
        # Leer el archivo CSV y cargar los datos en un DataFrame
        df = pd.read_csv(csv_file_path, sep=';', dtype=str, low_memory=False)

        current_time = datetime.now()

        # Reemplazar NaN con cadenas vacías en todos los campos
        df = df.fillna('')

        # Convertir campos específicos con cadenas vacías a 0
        numeric_columns_to_convert = [
            # 'score_tottus', 'precio_tottus',
            'score_lider', 'precio_lider',
            'score_jumbo', 'precio_jumbo'
        ]
        df[numeric_columns_to_convert] = df[numeric_columns_to_convert].apply(pd.to_numeric, errors='coerce')
        df = df.fillna(0)

        df['created_at'] = current_time.strftime("%Y-%m-%d %H:%M:%S")
        df['updated_at'] = current_time.strftime("%Y-%m-%d %H:%M:%S")

        # Delete all documents in the collection (Assuming conn is your MongoDB connection)
        conn.products.delete_many({})

        # Split the data into batches of 10,000 records and insert into MongoDB
        batch_size = 10000
        num_batches = math.ceil(len(df) / batch_size)

        for i in range(num_batches):
            start_idx = i * batch_size
            end_idx = (i + 1) * batch_size
            data_batch = df.iloc[start_idx:end_idx].to_dict(orient='records')
            # Insert data_batch into MongoDB (Assuming conn is your MongoDB connection)
            conn.products.insert_many(data_batch)


        return {'message': f'Datos insertados correctamente en MongoDB desde el archivo CSV: {csv_file_path}'}
    
    
    except Exception as e:  
        return {'Error': str(e)}
