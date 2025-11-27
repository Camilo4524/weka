import pandas as pd
import numpy as np
import random
from datetime import datetime

# Set random seed
np.random.seed(42)

n_rows = 300

# Helper to generate random dates
def random_dates(start, end, n):
    start_u = start.value//10**9
    end_u = end.value//10**9
    return pd.to_datetime(np.random.randint(start_u, end_u, n), unit='s')

start_date = pd.to_datetime('2023-01-01')
end_date = pd.to_datetime('2023-12-31')

data = {
    'MARCA_VEHICULO': np.random.choice(['CHEVROLET', 'RENAULT', 'MAZDA', 'TOYOTA', 'KIA', 'NISSAN'], n_rows),
    'MODELO_VEHICULO': np.random.choice(['SPARK', 'LOGAN', '3', 'HILUX', 'PICANTO', 'VERSA'], n_rows),
    'TIPO_VEHICULO': np.random.choice(['AUTOMOVIL', 'BUS', 'CAMION', 'MOTOCICLETA'], n_rows),
    'EDAD_VEHICULO': np.random.randint(0, 30, n_rows),
    'FECHA_ACCIDENTE': random_dates(start_date, end_date, n_rows),
    'DEPARTAMENTO_ACCIDENTE': np.random.choice(['ANTIOQUIA', 'CUNDINAMARCA', 'VALLE', 'ATLANTICO'], n_rows),
    'MUNICIPIO_ACCIDENTE': np.random.choice(['MEDELLIN', 'BOGOTA', 'CALI', 'BARRANQUILLA'], n_rows),
    'AUTORIDAD_DE_TRANSITO': np.random.choice(['SECRETARIA DE MOVILIDAD', 'POLICIA DE CARRETERAS'], n_rows)
}

df = pd.DataFrame(data)

# Logic for Target Variable (GRAVEDAD_ACCIDENTE)
# We want to create patterns the Random Forest can learn.
# 1. Motorcycles + Old Age -> High chance of 'CON MUERTOS'
# 2. Bus/Camion -> High chance of 'CON HERIDOS'
# 3. New Automovils -> 'SOLO DANOS'

conditions = [
    (df['TIPO_VEHICULO'] == 'MOTOCICLETA') & (df['EDAD_VEHICULO'] > 15),
    (df['TIPO_VEHICULO'].isin(['BUS', 'CAMION'])),
    (df['TIPO_VEHICULO'] == 'AUTOMOVIL') & (df['EDAD_VEHICULO'] < 5)
]

choices = ['CON MUERTOS', 'CON HERIDOS', 'SOLO DANOS']

# Default to random if no condition met
df['GRAVEDAD_ACCIDENTE'] = np.select(conditions, choices, default='SOLO DANOS')

# Add some noise
mask = np.random.random(n_rows) < 0.2
df.loc[mask, 'GRAVEDAD_ACCIDENTE'] = np.random.choice(['CON HERIDOS', 'SOLO DANOS'], size=mask.sum())

df.to_excel('datos_prediccion.xlsx', index=False)
print("datos_prediccion.xlsx created with 'CON MUERTOS' cases.")
