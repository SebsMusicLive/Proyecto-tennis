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

class LiveMatchState(rx.State):
    matches: list[Match] = []

    def load_matches(self):
        data = get_live_matches()

        # Extrae la lista de partidos desde la clave 'events'
        raw_matches = data.get("events", [])

        parsed_matches = []

        for match in raw_matches:
            try:
                # Datos del jugador local
                home_data = match.get("home", {})
                away_data = match.get("away", {})
                round_data = match.get("roundInfo", {})

                home_name = home_data.get("name", "Desconocido")
                away_name = away_data.get("name", "Desconocido")
                round_name = round_data.get("name", "Sin ronda")
                ts = match.get("startTimestamp", 0)

                # Formatear la hora de inicio
                formatted_time = (
                    datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M')
                    if ts else "Sin hora"
                )

                # Imagen del jugador local (si está disponible)
                home_image = (
                    home_data.get("image")
                    or home_data.get("team", {}).get("image")
                    or ""
                )

                parsed_matches.append(
                    Match(
                        HOME_NAME=home_name,
                        AWAY_NAME=away_name,
                        ROUND=round_name,
                        START_TIME=ts,
                        FORMATTED_TIME=formatted_time,
                        HOME_IMAGES=[home_image] if home_image else [],
                    )
                )
            except Exception as e:
                print(f"❌ Error al procesar el partido: {e}")
                continue

        self.matches = parsed_matches
