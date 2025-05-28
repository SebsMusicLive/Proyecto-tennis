# backend/live_state.py

import reflex as rx
import datetime
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
    MATCH_STATUS: str = ""     # Ej: "2nd set"
    STATUS_TYPE: str = ""      # Ej: "inprogress"
    HOME_COUNTRY: str = ""

class LiveMatchState(rx.State):
    matches: list[Match] = []

    def load_matches(self):
        data = get_live_matches()
        raw_matches = data.get("events", [])

        parsed_matches = []

        for match in raw_matches:
            try:
                home_data = match.get("home", match.get("homeTeam", {}))
                away_data = match.get("away", match.get("awayTeam", {}))

                round_data = match.get("roundInfo", {})
                status = match.get("status", {})
                season = match.get("season", {})

                home_name = home_data.get("name", "Desconocido")
                away_name = away_data.get("name", "Desconocido")
                round_name = str(round_data.get("round", "Sin ronda"))
                ts = match.get("startTimestamp", 0)

                formatted_time = (
                    datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M')
                    if ts else "Sin hora"
                )

                home_image = (
                    home_data.get("image")
                    or home_data.get("team", {}).get("image")
                    or ""
                )

                home_country = home_data.get("country", {}).get("name", "")

                parsed_matches.append(
                    Match(
                        HOME_NAME=home_name,
                        AWAY_NAME=away_name,
                        ROUND=round_name,
                        START_TIME=ts,
                        FORMATTED_TIME=formatted_time,
                        HOME_IMAGES=[home_image] if home_image else [],
                        TOURNAMENT_NAME=season.get("name", ""),
                        TOURNAMENT_YEAR=season.get("year", ""),
                        MATCH_STATUS=status.get("description", ""),
                        STATUS_TYPE=status.get("type", ""),
                        HOME_COUNTRY=home_country
                    )
                )
            except Exception as e:
                print(f"❌ Error al procesar el partido: {e}")
                continue

        self.matches = parsed_matches
