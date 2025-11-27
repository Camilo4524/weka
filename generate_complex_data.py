import pandas as pd
import numpy as np
import random

# Set random seed for reproducibility
np.random.seed(42)

# Generate 100 rows of data
n_rows = 100

data = {
    'EDAD_VEHICULO': np.random.randint(1, 20, n_rows),
    'TIPO_VEHICULO': np.random.choice(['AUTOMOVIL', 'BUS', 'CAMION', 'MOTOCICLETA'], n_rows),
    'MARCA_VEHICULO': np.random.choice(['CHEVROLET', 'RENAULT', 'MAZDA', 'TOYOTA', 'KIA'], n_rows),
    'GRAVEDAD_ACCIDENTE': np.random.choice(['CON HERIDOS', 'SOLO DANOS'], n_rows, p=[0.3, 0.7]),
    'VELOCIDAD_ESTIMADA': np.random.normal(60, 15, n_rows).astype(int)
}

df = pd.DataFrame(data)

# Introduce some nulls
df.loc[np.random.choice(df.index, 10), 'EDAD_VEHICULO'] = np.nan
df.loc[np.random.choice(df.index, 5), 'VELOCIDAD_ESTIMADA'] = np.nan

# Create a target variable for Linear Regression (Severity Index - synthetic)
# Severity increases with age and speed
df['INDICE_SEVERIDAD'] = (df['EDAD_VEHICULO'].fillna(10) * 0.5) + (df['VELOCIDAD_ESTIMADA'].fillna(60) * 0.1) + np.random.normal(0, 2, n_rows)

# Create a target variable for Logistic Regression (Binary)
# 1 if 'CON HERIDOS', 0 if 'SOLO DANOS'
df['GRAVEDAD_CODIFICADA'] = (df['GRAVEDAD_ACCIDENTE'] == 'CON HERIDOS').astype(int)

df.to_csv('traffic_data.csv', index=False)
print("traffic_data.csv created with nulls and categorical data.")
