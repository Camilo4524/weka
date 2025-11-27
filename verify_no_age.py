import requests

BASE_URL = "http://localhost:8000"

def verify_prediction_no_age():
    print("--- Verifying Prediction (No Age) ---")
    
    # 1. Ensure data is loaded (Trigger training)
    print("Loading data...")
    requests.get(f"{BASE_URL}/analyze")
    
    # 2. Make Prediction
    # Using 'MOTOCICLETA' which we know has high risk in our test data
    payload = {
        "type": "MOTOCICLETA",
        "brand": "CHEVROLET", # Just a placeholder, model should handle it
        "model": "SPARK"      # Just a placeholder
    }
    
    print(f"Sending Prediction Request: {payload}")
    
    try:
        response = requests.post(f"{BASE_URL}/predict", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print(f"Success! Prediction Status: {result['status']}")
        else:
            print(f"Failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_prediction_no_age()
