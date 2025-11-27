import requests
import pandas as pd
import json

BASE_URL = "http://localhost:8000"
FILE_PATH = "traffic_data.csv"

def run_verification():
    print("--- Starting Backend Verification ---")

    # 1. Upload File
    print(f"\n1. Uploading {FILE_PATH}...")
    with open(FILE_PATH, 'rb') as f:
        files = {'file': (FILE_PATH, f, 'text/csv')}
        response = requests.post(f"{BASE_URL}/upload", files=files)
    
    if response.status_code != 200:
        print(f"Upload Failed: {response.text}")
        return
    
    summary = response.json()
    print(f"Upload Success! Total rows: {summary['total_rows']}")
    print(f"Null counts: {summary['null_counts']}")

    # 2. Clean Data (Impute Median)
    print("\n2. Cleaning Data (Imputing Median)...")
    clean_req = {"action": "impute_median"}
    response = requests.post(f"{BASE_URL}/data/clean", json=clean_req)
    if response.status_code == 200:
        print("Cleaning Success! Nulls should be gone.")
    else:
        print(f"Cleaning Failed: {response.text}")

    # 3. Encode Data (One-Hot TIPO_VEHICULO)
    print("\n3. Encoding 'TIPO_VEHICULO'...")
    encode_req = {"columns": ["TIPO_VEHICULO"]}
    response = requests.post(f"{BASE_URL}/data/encode", json=encode_req)
    if response.status_code == 200:
        print("Encoding Success!")
        # print("New columns:", response.json()['columns'])
    else:
        print(f"Encoding Failed: {response.text}")

    # 4. Train Linear Regression
    print("\n4. Training Linear Regression Model...")
    # Target: INDICE_SEVERIDAD
    # Features: EDAD_VEHICULO, VELOCIDAD_ESTIMADA
    train_req = {
        "model_type": "linear",
        "x_columns": ["EDAD_VEHICULO", "VELOCIDAD_ESTIMADA"],
        "y_column": "INDICE_SEVERIDAD",
        "test_size": 0.2
    }
    response = requests.post(f"{BASE_URL}/models/train", json=train_req)
    
    if response.status_code == 200:
        result = response.json()
        print("Training Success!")
        print(f"R2 Score: {result['metrics']['r2_score']:.4f}")
        print(f"MSE: {result['metrics']['mse']:.4f}")
        print(f"Coefficients: {result['metrics']['coefficients']}")
    else:
        print(f"Training Failed: {response.text}")

    # 5. Train Logistic Regression
    print("\n5. Training Logistic Regression Model...")
    # Target: GRAVEDAD_CODIFICADA
    # Features: EDAD_VEHICULO, VELOCIDAD_ESTIMADA
    train_req_log = {
        "model_type": "logistic",
        "x_columns": ["EDAD_VEHICULO", "VELOCIDAD_ESTIMADA"],
        "y_column": "GRAVEDAD_CODIFICADA",
        "test_size": 0.2
    }
    response = requests.post(f"{BASE_URL}/models/train", json=train_req_log)
    
    if response.status_code == 200:
        result = response.json()
        print("Training Success!")
        print(f"Accuracy: {result['metrics']['accuracy']:.4f}")
        print(f"F1 Score: {result['metrics']['f1_score']:.4f}")
    else:
        print(f"Training Failed: {response.text}")

if __name__ == "__main__":
    try:
        run_verification()
    except Exception as e:
        print(f"Verification script failed: {e}")
