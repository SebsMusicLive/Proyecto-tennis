# backend/live_state.py

import reflex as rx
import datetime
import json # Añadido para imprimir el primer partido crudo
from ..backend.api_client import get_live_matches

# Modelo para representar un partido en vivo
class Match(rx.Base):
    HOME_NAME: str
    AWAY_NAME: str
    ROUND: str
    START_TIME: int
    FORMATTED_TIME: str = "Sin hora"
    HOME_IMAGES: list[str] = []

    # Nuevos campos agregados
    TOURNAMENT_NAME: str = ""
    TOURNAMENT_YEAR: str = ""
    MATCH_STATUS: str = ""      # Ej: "2nd set"
    STATUS_TYPE: str = ""        # Ej: "inprogress"
    HOME_COUNTRY: str = ""

class LiveMatchState(rx.State):
    matches: list[Match] = []

    def load_matches(self):
        data = get_live_matches()
        raw_matches = data.get("events", [])

        parsed_matches = []

        if not raw_matches:
            print("ℹ️ No se encontraron partidos en vivo.")
            self.matches = []
            return

        # Tomar solo el primer partido de la lista
        first_raw_match = raw_matches[0]

        # ---- INICIO: Para entender la estructura del primer partido ----
        print("\n🔍 Estructura del primer partido (datos crudos):")
        print(json.dumps(first_raw_match, indent=2))
        # ---- FIN: Para entender la estructura del primer partido ----

        try:
            # Procesar únicamente el primer partido
            match = first_raw_match # Renombramos para mantener consistencia con el código original del bucle

            home_data = match.get("homeTeam", {}) # Corregido para ser consistente con la respuesta común de esta API
            away_data = match.get("awayTeam", {}) # Corregido para ser consistente

            # Intentar obtener 'tournament' y luego 'season' como fallback para el nombre y año del torneo
            tournament_data = match.get("tournament", {})
            season_data = match.get("season", {}) # 'season' puede estar dentro de 'tournament' o al mismo nivel que 'tournament'

            round_data = match.get("roundInfo", {})
            status = match.get("status", {})


            home_name = home_data.get("name", "Desconocido")
            away_name = away_data.get("name", "Desconocido")
            
            round_name = "Sin ronda"
            if isinstance(round_data, dict): # Verificar si round_data es un diccionario
                round_name = str(round_data.get("round", "Sin ronda"))
            elif isinstance(round_data, str): # Si round_data es directamente un string
                round_name = round_data


            ts = match.get("startTimestamp", 0)

            formatted_time = (
                datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
                if ts else "Sin hora"
            )
            
            # Es común que 'id' del equipo se use para formar la URL de la imagen.
            # El formato exacto de la URL de la imagen depende de la API y cómo sirve los assets.
            # Este es un intento genérico; necesitarás verificar la estructura de 'homeTeam.id' y la URL base de imágenes.
            home_team_id = home_data.get("id")
            home_image_url = ""
            if home_team_id:
                # Ejemplo de URL, ajusta según la API:
                home_image_url = f"https://api.sofascore.com/api/v1/team/{home_team_id}/image"


            home_country_data = home_data.get("country", {})
            home_country = home_country_data.get("name", "") if isinstance(home_country_data, dict) else ""


            # Intentar obtener el nombre del torneo y año
            tournament_name = tournament_data.get("name", "")
            tournament_category = tournament_data.get("category", {}).get("name", "")
            if tournament_category and tournament_name: # Combinar nombre y categoría si ambos existen
                tournament_name = f"{tournament_name} - {tournament_category}"
            elif not tournament_name: # Fallback a season si tournament_name está vacío
                tournament_name = season_data.get("name", "Torneo Desconocido")


            tournament_year = str(tournament_data.get("season", {}).get("year", "")) # Intentar desde tournament -> season -> year
            if not tournament_year: # Fallback a season_data a nivel de match
                tournament_year = str(season_data.get("year", datetime.datetime.now().year))


            parsed_matches.append(
                Match(
                    HOME_NAME=home_name,
                    AWAY_NAME=away_name,
                    ROUND=round_name,
                    START_TIME=ts,
                    FORMATTED_TIME=formatted_time,
                    HOME_IMAGES=[home_image_url] if home_image_url else [],
                    TOURNAMENT_NAME=tournament_name,
                    TOURNAMENT_YEAR=tournament_year,
                    MATCH_STATUS=status.get("description", "Estado Desconocido"),
                    STATUS_TYPE=status.get("type", "unknown"),
                    HOME_COUNTRY=home_country
                )
            )
        except Exception as e:
            print(f"❌ Error al procesar el primer partido: {e}")
            # Si hay un error, la lista parsed_matches quedará vacía

        self.matches = parsed_matches

# Ejemplo de cómo podrías ejecutarlo para probar (si este archivo fuera el principal)
if __name__ == "__main__":
    # Para probar, necesitarías configurar el entorno de Reflex o simularlo.
    # Esta es una forma simplificada de ver la salida:
    
    # Mock de la función get_live_matches si no quieres hacer la llamada real
    # o si necesitas que la API_KEY esté configurada.
    def get_live_matches_mock():
        # Pega aquí una respuesta de ejemplo de tu API si la tienes
        return {
            "events": [
                {
                    "tournament": {
                        "name": "Roland Garros",
                        "category": {"name": "Grand Slam"},
                        "season": {"year": "2024"}
                    },
                    "roundInfo": {"round": 128}, # Ejemplo, podría ser "Finals", "Semifinals"
                    "customId": "sMfcsgOEc",
                    "status": {"code": 100, "description": "Finished", "type": "finished"},
                    "winnerCode": 1,
                    "homeTeam": {
                        "name": "Alcaraz C.",
                        "slug": "alcaraz-carlos",
                        "gender": "M",
                        "country": {
                            "alpha2": "ES",
                            "name": "Spain"
                        },
                        "subTeams": [],
                        "teamColors": {"primary": "#52b030", "secondary": "#52b030", "text": "#ffffff"},
                        "id": 785576,
                        "countryId": 32,
                        "disabled": None,
                        "type": 1
                    },
                    "awayTeam": {
                        "name": "Zverev A.",
                        "slug": "zverev-alexander",
                        "gender": "M",
                        "country": {
                            "alpha2": "DE",
                            "name": "Germany"
                        },
                        "subTeams": [],
                        "teamColors": {"primary": "#52b030", "secondary": "#52b030", "text": "#ffffff"},
                        "id": 201103,
                        "countryId": 3,
                        "disabled": None,
                        "type": 1
                    },
                    "homeScore": {"current": 3, "display": 3, "period1": 6, "period2": 2, "period3": 5, "period4": 6, "period5": 6, "normaltime": 3},
                    "awayScore": {"current": 2, "display": 2, "period1": 3, "period2": 6, "period3": 7, "period4": 1, "period5": 2, "normaltime": 2},
                    "time": {},
                    "changes": {"changes": ["event.liveTimestamp. સુયોજિત નથી"], "changeTimestamp": 1717960683},
                    "hasGlobalHighlights": True,
                    "hasEventPlayerStatistics": True,
                    "hasEventPlayerHeatMap": True,
                    "crowdsourcingDataDisplayEnabled": False,
                    "id": 12358106,
                    "season": {"name": "Roland Garros", "year": "2024", "editor": False, "id": 52431}, # Ejemplo de season a nivel de match
                    "defaultTournament": {"id": 1012, "name": "Roland Garros", "slug": "roland-garros", "category": {"id": 4, "name": "Grand Slam", "slug": "grand-slam", "sport": {"id": 5, "name": "Tennis", "slug": "tennis"}, "flag": "grandslam", "alpha2": None}, "uniqueTournament": {"id": 71, "name": "Roland Garros", "slug": "roland-garros", "userCount": 273335, "crowdsourcingEnabled": False, "hasPerformanceGraphFeature": False, "displayInverseHomeAwayTeams": False, "priority": 932, "competitionType": 2, "primaryColorHex": "#e8702b", "secondaryColorHex": "#b0501c", "country": {}}, "displayInverseHomeAwayTeams": False},
                    "startTimestamp": 1717941600,
                    "slug": "zverev-alcaraz-c",
                    "finalResultOnly": False,
                    "isEditor": False,
                    "crowdsourcingEnabled": False
                },
                # ... otros partidos que serán ignorados ...
            ]
        }

    # Comenta la siguiente línea si quieres usar la llamada real a la API
    # y tienes tu RAPIDAPI_KEY configurada en el entorno.
    original_get_live_matches = get_live_matches
    globals()['get_live_matches'] = get_live_matches_mock # Sobreescribe temporalmente para prueba

    state = LiveMatchState()
    state.load_matches()

    if state.matches:
        print("\n✅ Datos del primer partido procesado:")
        # rx.Base no tiene un __str__ o __repr__ útil por defecto para print,
        # así que lo convertimos a dict para una mejor visualización
        # o accedemos a los campos individualmente.
        first_match_obj = state.matches[0]
        print(f"  Torneo: {first_match_obj.TOURNAMENT_NAME} ({first_match_obj.TOURNAMENT_YEAR})")
        print(f"  Partido: {first_match_obj.HOME_NAME} vs {first_match_obj.AWAY_NAME}")
        print(f"  Ronda: {first_match_obj.ROUND}")
        print(f"  Hora: {first_match_obj.FORMATTED_TIME}")
        print(f"  Estado: {first_match_obj.MATCH_STATUS} ({first_match_obj.STATUS_TYPE})")
        print(f"  País Local: {first_match_obj.HOME_COUNTRY}")
        print(f"  Imágenes Local: {first_match_obj.HOME_IMAGES}")

    else:
        print("🚫 No se procesó ningún partido.")
    
    globals()['get_live_matches'] = original_get_live_matches # Restaura la función original