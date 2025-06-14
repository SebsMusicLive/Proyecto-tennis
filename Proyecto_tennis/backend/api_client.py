# backend/api_client.py

import httpx
import os
import json

SPORTRADAR_API_KEY = os.getenv("SPORTRADAR_API_KEY", "vWP7ABNOagUPu3vEAkZqFdN6t6fW5lZiSYP7UzPA")

HEADERS = {
    "accept": "application/json",
    "x-api-key": SPORTRADAR_API_KEY
}

def get_live_matches():
    # ... (tu código existente para get_live_matches) ...
    url = "https://api.sportradar.com/tennis/trial/v3/en/schedules/live/summaries.json"
    try:
        response = httpx.get(url, headers=HEADERS)
        response.raise_for_status()

        data = response.json()

        # 🟡 DEBUG opcional: imprime toda la respuesta
        # print("\n----- Respuesta COMPLETA de Sportradar (api_client.py) -----")
        # print(json.dumps(data, indent=2))
        # print("----------------------------------------------------\n")

        return data
    except Exception as e:
        print("❌ Error al consumir la API:", e)
        return {}


# 🚨 ASEGÚRATE DE QUE ESTA FUNCIÓN ESTÉ AQUÍ Y BIEN DEFINIDA
def get_head_to_head_stats(competitor1_id: str, competitor2_id: str):
    """
    Obtiene estadísticas Head-to-Head entre dos competidores de la API de Sportradar.
    Requiere IDs de competidores.
    """
    if not competitor1_id or not competitor2_id:
        print("❌ Error: Se requieren ambos IDs de competidores para H2H.")
        return {}

    # Asegúrate de que este es el endpoint correcto de H2H para tu paquete de API
    # Este es un ejemplo común, pero VERIFICA TU DOCUMENTACIÓN DE SPORTRADAR
    url = f"https://api.sportradar.com/tennis/trial/v3/en/competitors/{competitor1_id}/vs/{competitor2_id}/summaries.json"

    try:
        response = httpx.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        # 🟡 DEBUG opcional: imprime la respuesta H2H completa
        # print(f"\n----- Respuesta H2H para {competitor1_id} vs {competitor2_id} -----")
        # print(json.dumps(data, indent=2))
        # print("----------------------------------------------------\n")
        return data
    except Exception as e:
        print(f"❌ Error al obtener estadísticas H2H para {competitor1_id} vs {competitor2_id}: {e}")
        return {}