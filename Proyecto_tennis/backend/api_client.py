# backend/api_client.py

import httpx
import os

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "ea3487d304mshc57f788e9c05a9cp141100jsn121ec8ce9040")
RAPIDAPI_HOST = "tennisapi1.p.rapidapi.com"

HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": RAPIDAPI_HOST
}

def get_live_matches():
    url = "https://tennisapi1.p.rapidapi.com/api/tennis/events/live"
    try:
        response = httpx.get(url, headers=HEADERS)
        response.raise_for_status()

        data = response.json()

        # 🟢 Verifica el tipo de estructura de respuesta (esto ayuda al depurado)
        print("📦 Tipo de respuesta:", type(data))
        print("📨 Claves de la respuesta:", data.keys())

        return data
    except Exception as e:
        print("❌ Error al consumir la API:", e)
        return {}
