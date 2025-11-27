import requests

BASE_URL = "http://localhost:8000"

def verify_auto_load():
    print("--- Verifying Auto-Load ---")
    
    try:
        # Call GET /analyze
        response = requests.get(f"{BASE_URL}/analyze")
        
        if response.status_code == 200:
            data = response.json()
            print("Success! Data loaded automatically.")
            
            # Check Linear Analysis
            if data.get('linear_analysis'):
                print(f"Linear Analysis: {data['linear_analysis']['answer']}")
            else:
                print("Linear Analysis: Not enough data (Expected if file is empty/small)")
                
            # Check Dropdowns
            options = data.get('dropdown_options', {})
            print(f"Dropdowns Loaded: {list(options.keys())}")
            print(f"Vehicle Types: {len(options.get('TIPO_VEHICULO', []))}")
            
        else:
            print(f"Failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_auto_load()
