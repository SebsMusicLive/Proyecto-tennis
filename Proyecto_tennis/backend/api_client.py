import httpx

RAPIDAPI_KEY = "ea3487d304mshc57f788e9c05a9cp141100jsn121ec8ce9040"
RAPIDAPI_HOST = "tennisapi1.p.rapidapi.com"

HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": RAPIDAPI_HOST
}

def get_live_matches():
    url = "https://tennisapi1.p.rapidapi.com/api/tennis/rankings/wta/live"
    params = {
        "sport_id": "2",                # tenis
        "locale": "es_ES",
        "timezone": "-5",
        "indent_days": "0"              # <-- importante: usar 0 para el día actual
    }

    try:
        response = httpx.get(url, headers=HEADERS, params=params)
        print("🔗 URL:", response.url)
        print("📦 Status code:", response.status_code)
        print("📨 Response text:", response.text)
        
        data = response.json()

        # 🔍 Agrega estas dos líneas:
        print("🔎 Tipo de respuesta:", type(data))
        print("🔎 Contenido de la respuesta:", data)

        return data
    except Exception as e:
        print("❌ Error al consumir la API:", e)
        return {"events": []}