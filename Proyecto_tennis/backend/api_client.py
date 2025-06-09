# backend/api_client.py

import httpx
import os
import json

# Clave de la API de Sportradar. Es una buena práctica usar variables de entorno.
# Si no la tienes configurada como variable de entorno, puedes ponerla directamente aquí,
# pero se recomienda usar os.getenv para mayor seguridad y flexibilidad.
SPORTRADAR_API_KEY = os.getenv("SPORTRADAR_API_KEY", "vWP7ABNOagUPu3vEAkZqFdN6t6fW5lZiSYP7UzPA")

HEADERS = {
    "accept": "application/json",
    "x-api-key": SPORTRADAR_API_KEY
}

def get_live_matches():
    """
    Obtiene un resumen de los partidos de tenis en vivo de la API de Sportradar.
    """
    url = "https://api.sportradar.com/tennis/trial/v3/es/seasons/sr%3Aseason%3A107797/info.json"
    try:
        response = httpx.get(url, headers=HEADERS)
        response.raise_for_status()  # Lanza una excepción para códigos de estado HTTP 4xx/5xx

        data = response.json()

        # 🟡 DEBUG opcional: imprime toda la respuesta para inspeccionarla
        # print(json.dumps(data, indent=2))

        return data
    except httpx.RequestError as e:
        print(f"❌ Error de red o conexión al consumir la API de Sportradar: {e}")
        return {}
    except httpx.HTTPStatusError as e:
        print(f"❌ Error en la respuesta HTTP de la API de Sportradar: {e.response.status_code} - {e.response.text}")
        return {}
    except json.JSONDecodeError:
        print("❌ Error al decodificar la respuesta JSON de la API de Sportradar.")
        return {}
    except Exception as e:
        print(f"❌ Ocurrió un error inesperado: {e}")
        return {}

# Ejemplo de cómo usar la función (solo para pruebas)
if __name__ == "__main__":
    print("Obteniendo partidos en vivo de Sportradar...")
    live_data = get_live_matches()
    if live_data:
        # Aquí puedes procesar la 'live_data' como necesites
        print("\nDatos de partidos en vivo obtenidos exitosamente (resumen):")
        # Por ejemplo, si sabes que la estructura es 'summaries', puedes iterar sobre ellos
        if 'summaries' in live_data:
            for match_summary in live_data['summaries']:
                # Aquí puedes acceder a la información específica de cada partido
                # La estructura exacta dependerá de la respuesta de Sportradar
                # Puedes imprimir el JSON completo en el DEBUG opcional para ver la estructura
                # Por ejemplo, si hay 'sport_event', 'competitors', etc.
                if 'sport_event' in match_summary and 'competitors' in match_summary['sport_event']:
                    competitors = match_summary['sport_event']['competitors']
                    if len(competitors) == 2:
                        print(f"  Partido: {competitors[0]['name']} vs {competitors[1]['name']}")
                    else:
                        print(f"  Partido ID: {match_summary['sport_event']['id']}")
                else:
                    print(f"  Resumen de evento sin detalles completos: {match_summary.get('sport_event', {}).get('id', 'N/A')}")
        else:
            print("La respuesta de la API no contiene la clave 'summaries'.")
            print(json.dumps(live_data, indent=2)) # Imprime la estructura si no es lo esperado
    else:
        print("No se pudieron obtener datos de partidos en vivo.")