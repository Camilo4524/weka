import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Set random seed
np.random.seed(42)

n_rows = 200

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

# Logic: Older vehicles have slightly higher chance of injury accidents
# Base probability of injury
probs = []
for age in df['EDAD_VEHICULO']:
    # Probability increases with age: 0.2 base + 0.02 per year
    p_injury = min(0.2 + (age * 0.02), 0.9)
    probs.append(p_injury)

df['GRAVEDAD_ACCIDENTE'] = [np.random.choice(['CON HERIDOS', 'SOLO DANOS'], p=[p, 1-p]) for p in probs]

# Save
df.to_excel('datos_accidentes.xlsx', index=False)
print("datos_accidentes.xlsx created with specific columns.")
