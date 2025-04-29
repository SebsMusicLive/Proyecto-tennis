import httpx

RAPIDAPI_KEY = "ea3487d304mshc57f788e9c05a9cp141100jsn121ec8ce9040"
RAPIDAPI_HOST = "flashlive-sports.p.rapidapi.com"

HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": RAPIDAPI_HOST
}

BASE_URL = "https://flashlive-sports.p.rapidapi.com/v1/news/categories?locale=en_INT"

def get_live_matches():
    url = f"{BASE_URL}/events/list"
    params = {
        "sport_id": "2",  # 2 es el ID para tenis
    }

    try:
        response = httpx.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("❌ Error al consumir la API:", e)
        return {"events": []}
