import requests
import itertools

BASE_URL = "http://localhost:8000"

def find_death_case():
    print("--- Buscando caso 'MUERTO' ---")
    
    # 1. Load Data to get options
    try:
        response = requests.get(f"{BASE_URL}/analyze")
        if response.status_code != 200:
            print("Error loading data.")
            return
        
        options = response.json().get('dropdown_options', {})
        types = options.get('TIPO_VEHICULO', [])
        brands = options.get('MARCA_VEHICULO', [])
        models = options.get('MODELO_VEHICULO', [])
        
        print(f"Opciones cargadas: {len(types)} Tipos, {len(brands)} Marcas, {len(models)} Modelos")
        
        # Prioritize searching 'MOTOCICLETA' as it's most likely to have high severity
        if 'MOTOCICLETA' in types:
            types = ['MOTOCICLETA'] + [t for t in types if t != 'MOTOCICLETA']
            
        # Limit search space to avoid infinite loop if too large
        # We'll try a subset
        count = 0
        max_tries = 500
        
        for t in types:
            for b in brands:
                for m in models:
                    count += 1
                    if count > max_tries:
                        print("Límite de búsqueda alcanzado sin éxito.")
                        return

                    payload = {
                        "type": t,
                        "brand": b,
                        "model": m
                    }
                    
                    try:
                        res = requests.post(f"{BASE_URL}/predict", json=payload)
                        if res.status_code == 200:
                            status = res.json()['status']
                            if status == 'MUERTO':
                                print("\n¡ENCONTRADO!")
                                print(f"Para obtener 'MUERTO', seleccione:")
                                print(f"Tipo: {t}")
                                print(f"Marca: {b}")
                                print(f"Modelo: {m}")
                                return
                    except:
                        pass
                        
        print("No se encontró ningún caso 'MUERTO' en la búsqueda limitada.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    find_death_case()
